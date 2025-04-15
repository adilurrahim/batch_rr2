import os
import time
import geopandas as gpd
import pandas as pd
import rasterio
from shapely.geometry import Point
import numpy as np
from tqdm.auto import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
from helper_functions import get_single_value, get_multiple_values, get_elevation, get_sre, get_distance_to_coast, process_huc_data
import warnings
warnings.filterwarnings("ignore")

def process_chunk(chunk_df, year, plan, scenario, base_path,  projected_crs = 'EPSG:26915'):
    """
    Worker function to process a chunk of the input dataframe.
    Loads required shapefiles and raster data, calculates geographic attributes for each point,
    and returns the result along with the time elapsed.
    """
    start_time = time.perf_counter()
    
    # Define file paths
    county_shapefile_path = os.path.join(base_path, "CommonData", "County")
    crs_shapefile_path = os.path.join(base_path, "CommonData", "CRS")
    flowline_shapefile_path = os.path.join(base_path, "CommonData", "FlowLine")
    huc12_shapefile_path = os.path.join(base_path, "CommonData", "HUC12")
    river_poly_shapefile_path = os.path.join(base_path, "CommonData", "RiverPolygon")
    
    elevation_raster_path = os.path.join(base_path, "ScenarioSpecificData", str(year), plan, scenario, "Elevation")
    levee_shapefile_path = os.path.join(base_path, "ScenarioSpecificData", str(year), plan, scenario, "Levee")
    flood_depth_raster_path = os.path.join(base_path, "ScenarioSpecificData", str(year), plan, scenario, "FloodDepth")
    coastline_shapefile_path = os.path.join(base_path, "ScenarioSpecificData", str(year), plan, scenario, "CoastLine")
    
    # Load vector datasets
    coastline_gdf_proj = gpd.read_file(os.path.join(coastline_shapefile_path, "CoastLine.shp")).to_crs(projected_crs)
    riverpoly_gdf_proj = gpd.read_file(os.path.join(river_poly_shapefile_path, "RiverPolygon.shp")).to_crs(projected_crs)
    flowline_gdf_proj = gpd.read_file(os.path.join(flowline_shapefile_path, "FlowLine.shp")).to_crs(projected_crs)
    county_gdf = gpd.read_file(os.path.join(county_shapefile_path, "County.shp"))
    huc12_gdf = gpd.read_file(os.path.join(huc12_shapefile_path, "HUC12.shp"))
    crs_gdf = gpd.read_file(os.path.join(crs_shapefile_path, "CRS.shp"))
    levee_gdf = gpd.read_file(os.path.join(levee_shapefile_path, "Levee.shp"))
    
    # Load elevation raster data
    elevation_file = [f for f in os.listdir(elevation_raster_path) if "projected" in f][0]
    elevation_dataset = rasterio.open(os.path.join(elevation_raster_path, elevation_file))
    elevation_band = elevation_dataset.read(1)
    
    # Load flood depth rasters
    fd_100_file = [f for f in os.listdir(flood_depth_raster_path) if "1.0" in f][0]
    fd_10_file = [f for f in os.listdir(flood_depth_raster_path) if "10.0" in f][0]
    fd_100_dataset = rasterio.open(os.path.join(flood_depth_raster_path, fd_100_file))
    fd_10_dataset = rasterio.open(os.path.join(flood_depth_raster_path, fd_10_file))
    
    results = []
    # Process each row in the chunk
    for _, row in chunk_df.iterrows():
        point = Point(row['lon'], row['lat'])
        point_gdf = gpd.GeoDataFrame(geometry=[point], crs='EPSG:4269')
        point_gdf_proj = point_gdf.to_crs(projected_crs)
    
        county_name = get_single_value(county_gdf, point, 'NAME')
        crs_val = get_multiple_values(crs_gdf, point_gdf_proj, 'CRS_Class')
        levee = get_multiple_values(levee_gdf, point_gdf_proj, 'systemId')
        huc12_name = get_single_value(huc12_gdf, point, 'HUC12')
    
        elevation = get_elevation(elevation_dataset, elevation_band, point_gdf_proj)
        sre = get_sre(elevation_dataset, point_gdf_proj)
        distance_to_coast = get_distance_to_coast(point_gdf_proj, coastline_gdf_proj)
    
        DTR, RiverElevation, ERR, DA, FloodDepthDifference = process_huc_data(
            huc12_name, point_gdf_proj, elevation, elevation_dataset,
            elevation_band, fd_10_dataset, fd_100_dataset,
            riverpoly_gdf_proj, flowline_gdf_proj
        )
    
        result = {
            'structure_id': row['structure_id'],
            'County': county_name,
            'HUC12': huc12_name,
            'CRS': crs_val,
            'LeveeSystemId': levee,
            'Elevation': elevation,
            'StructRelElev': sre,
            'DTR': DTR,
            'ElevRiver': RiverElevation,
            'ERR': ERR,
            'DrainageArea': DA,
            'RiverClass': FloodDepthDifference,
            'DTC': distance_to_coast
        }
        results.append(result)
    
    elapsed_time = time.perf_counter() - start_time
    return results, elapsed_time

def extract_geographic_attributes_parallel(df, year, plan, scenario, base_path="data/ProcessedData", output_dir = "output",
                                  projected_crs='EPSG:26915', num_workers= os.cpu_count()//2):
    """
    Extract geographic attributes in parallel using a chunking strategy.
    Splits the input DataFrame across multiple processes, aggregates the results,
    and updates the tqdm progress bar with the time taken for each chunk.
    """
    df_chunks = np.array_split(df, num_workers)
    all_results = []
    chunk_times = {}
    
    overall_start = time.perf_counter()
    pbar = tqdm(total=len(df_chunks), desc=f"Extracting GA {year}-{plan}-{scenario}")
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = {
            executor.submit(process_chunk, chunk, year, plan, scenario, base_path, projected_crs): idx
            for idx, chunk in enumerate(df_chunks)
        }
        for future in as_completed(futures):
            chunk_idx = futures[future]
            try:
                chunk_results, elapsed_time = future.result()
                all_results.extend(chunk_results)
                chunk_times[chunk_idx] = elapsed_time
                # Update the progress bar's postfix to show the elapsed time of the current chunk
                pbar.set_postfix({f"Chunk {chunk_idx} time": f"{elapsed_time:.2f} sec"})
                pbar.update(1)
            except Exception as e:
                print(f"Error processing chunk {chunk_idx}: {e}")
    
    pbar.close()
    overall_elapsed = time.perf_counter() - overall_start
    print(f"\nTotal processing time: {overall_elapsed:.2f} seconds.")
    for idx, t in chunk_times.items():
        print(f" - Chunk {idx}: {t:.2f} sec")
    
    return pd.DataFrame(all_results)

