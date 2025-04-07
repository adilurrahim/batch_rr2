import os
import geopandas as gpd
import pandas as pd
import rasterio
from shapely.geometry import Point
import warnings
warnings.filterwarnings("ignore")
from helper_functions import *
from tqdm.auto import tqdm

def extract_geographic_attributes(df, year, plan, scenario, base_path = "data/ProcessedData",projected_crs = 'EPSG:26915'):
    ## Paths
    county_shapefile_path = os.path.join(base_path,"CommonData","County")
    crs_shapefile_path = os.path.join(base_path,"CommonData","CRS")
    flowline_shapefile_path = os.path.join(base_path,"CommonData","FlowLine")
    huc12_shapefile_path = os.path.join(base_path,"CommonData","HUC12")
    river_poly_shapefile_path = os.path.join(base_path,"CommonData","RiverPolygon")

    elevation_raster_path = os.path.join(base_path,"ScenarioSpecificData",str(year),plan,scenario,"Elevation")
    levee_shapefile_path = os.path.join(base_path,"ScenarioSpecificData",str(year),plan,scenario,"Levee")
    flood_depth_raster_path = os.path.join(base_path,"ScenarioSpecificData",str(year),plan,scenario,"FloodDepth")
    coastline_shapefile_path = os.path.join(base_path,"ScenarioSpecificData",str(year),plan,scenario,"CoastLine")

    ## Load datasets
    coastline_gdf_proj = gpd.read_file(coastline_shapefile_path + "/CoastLine.shp").to_crs(projected_crs)
    riverpoly_gdf_proj = gpd.read_file(river_poly_shapefile_path + "/RiverPolygon.shp").to_crs(projected_crs)
    flowline_gdf_proj = gpd.read_file(flowline_shapefile_path + "/FlowLine.shp").to_crs(projected_crs)
    county_gdf = gpd.read_file(county_shapefile_path + "/County.shp")
    huc12_gdf = gpd.read_file(huc12_shapefile_path + "/HUC12.shp")
    crs_gdf = gpd.read_file(crs_shapefile_path + "/CRS.shp")
    levee_gdf = gpd.read_file(levee_shapefile_path + "/Levee.shp")

    elevation_file = [f for f in os.listdir(elevation_raster_path) if "projected" in f][0]
    elevation_dataset = rasterio.open(os.path.join(elevation_raster_path, elevation_file))
    elevation_band = elevation_dataset.read(1)

    fd_100_files = [f for f in os.listdir(flood_depth_raster_path) if "1.0" in f][0]
    fd_10_files = [f for f in os.listdir(flood_depth_raster_path) if "10.0" in f][0]
    fd_100_dataset = rasterio.open(os.path.join(flood_depth_raster_path, fd_100_files))
    fd_10_dataset = rasterio.open(os.path.join(flood_depth_raster_path, fd_10_files))

    geographic_attr = []
    for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Extracting GA {year}-{plan}-{scenario}"):
        point = Point(row['lon'], row['lat'])
        point_gdf = gpd.GeoDataFrame(geometry=[point], crs='EPSG:4269')
        point_gdf_proj = point_gdf.to_crs(projected_crs)

        county_name = get_single_value(county_gdf, point, 'NAME')
        crs_val = get_multiple_values(crs_gdf, point, 'CRS_Class')
        levee = get_multiple_values(levee_gdf, point, 'systemId')
        huc12_name = get_single_value(huc12_gdf, point, 'HUC12')

        elevation = get_elevation(elevation_dataset, elevation_band, point_gdf_proj)
        sre = get_sre(elevation_dataset, point_gdf_proj)
        distance_to_coast = get_distance_to_coast(point_gdf_proj, coastline_gdf_proj)

        DTR, RiverElevation, ERR, DA, FloodDepthDifference = process_huc_data(
            huc12_name, point, point_gdf_proj, elevation, elevation_dataset,
            elevation_band, fd_10_dataset, fd_100_dataset,
            riverpoly_gdf_proj, flowline_gdf_proj)

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
        geographic_attr.append(result)

    return pd.DataFrame(geographic_attr)
