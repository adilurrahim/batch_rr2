from rasterio.mask import mask
import numpy as np
from shapely.ops import nearest_points
from shapely.geometry import Point
import geopandas as gpd
import pandas as pd
#helper functions
def get_single_value(gdf, point, column_name):
    subset = gdf[gdf.geometry.contains(point)]
    if len(subset) > 0:
        return subset.iloc[0][column_name]
    return np.nan
    
def get_multiple_values(gdf, point, column_name):
    subset = gdf[gdf.geometry.contains(point)]
    if len(subset) > 0:
        return subset[column_name].tolist()
    return []

def get_elevation(elevation_dataset, elevation_band, point_gdf_proj):
    x, y = point_gdf_proj.iloc[0].geometry.x, point_gdf_proj.iloc[0].geometry.y
    row, col = elevation_dataset.index(x, y)
    return elevation_band[row, col]
    

def get_sre(elevation_dataset, point_gdf_proj, point_crs='EPSG:4269', projected_crs = 'EPSG:26915', radius=500):
    """
    Computes SRE as the mean of elevation data in a buffer around the point.
    """
    x_proj, y_proj = point_gdf_proj.iloc[0].geometry.x, point_gdf_proj.iloc[0].geometry.y
    point_proj = Point(x_proj, y_proj)

    buffer_geom_proj = point_proj.buffer(500)
    raster_crs = elevation_dataset.crs
    buffer_geom_proj_gdf = gpd.GeoDataFrame(geometry=[buffer_geom_proj], crs=projected_crs)
    buffer_geom_raster_crs = buffer_geom_proj_gdf.to_crs(raster_crs)

    sre_out, _ = mask(elevation_dataset, buffer_geom_raster_crs.geometry, crop=True)
    sre_out = sre_out[0]
    valid_data = sre_out[sre_out != elevation_dataset.nodata]

    if valid_data.size > 0:
        return valid_data.mean()
    else:
        return np.nan

def get_distance_to_coast(point_gdf_proj, coastline_gdf_proj):
    """Returns the distance from the point to the coastline."""
    return coastline_gdf_proj.distance(point_gdf_proj.iloc[0].geometry).min()
 
    
def process_huc_data(huc12_name, point, point_gdf_proj, elevation, elevation_dataset, elevation_band, fd_10_dataset, fd_100_dataset, 
                             riverpoly_gdf_proj, flowline_gdf_proj, projected_crs = 'EPSG:26915'):
    """
    Given the HUC12 name, retrieves related attributes:
    DTR, ERR, DA, Flood Depth Difference.
    """
    if pd.isna(huc12_name):
        # No HUC data found
        return np.nan, np.nan, np.nan, np.nan, np.nan

    # Filter riverpoly and flowline by HUC12
    riverpoly_filtered = riverpoly_gdf_proj[riverpoly_gdf_proj['HUC12'] == huc12_name].copy()
    flowline_filtered = flowline_gdf_proj[flowline_gdf_proj['HUC12'] == huc12_name].copy()

    # Project to match projected CRS for distance calculations
    if len(riverpoly_filtered) > 0:
        riverpoly_filtered['distance'] = riverpoly_filtered.geometry.distance(point_gdf_proj.iloc[0].geometry)
        closest_riverpoly_feature = riverpoly_filtered.loc[riverpoly_filtered['distance'].idxmin()]
        distance_to_river = closest_riverpoly_feature['distance']
    else:
        closest_riverpoly_feature = None
        distance_to_river = np.nan

    if len(flowline_filtered) > 0:
        flowline_filtered['distance'] = flowline_filtered.geometry.distance(point_gdf_proj.iloc[0].geometry)
        closest_flowline_feature = flowline_filtered.loc[flowline_filtered['distance'].idxmin()]
        distance_to_flowline = closest_flowline_feature['distance']
    else:
        closest_flowline_feature = None
        distance_to_flowline = np.nan

    # Determine closest feature (river poly or flowline)
    if pd.notna(distance_to_river) and pd.notna(distance_to_flowline):
        if distance_to_river < distance_to_flowline:
            closest_feature_distance = distance_to_river
            closest_feature_geom = closest_riverpoly_feature
        else:
            closest_feature_distance = distance_to_flowline
            closest_feature_geom = closest_flowline_feature
    elif pd.notna(distance_to_river):
        closest_feature_distance = distance_to_river
        closest_feature_geom = closest_riverpoly_feature
    elif pd.notna(distance_to_flowline):
        closest_feature_distance = distance_to_flowline
        closest_feature_geom = closest_flowline_feature
    else:
        # No river or flowline
        closest_feature_distance = np.nan
        closest_feature_geom = None

    # Get ERR 
    if closest_feature_geom is not None:
        _,closest_geom_coords = nearest_points(point_gdf_proj.iloc[0].geometry, closest_feature_geom.geometry)
        
        closest_geom_coords_gdf = gpd.GeoDataFrame(geometry=[closest_geom_coords], crs=projected_crs)
        
        river_elev = get_elevation(elevation_dataset, elevation_band, closest_geom_coords_gdf) 
        err = elevation - river_elev
    else:
        river_elev = np.nan
        err = np.nan

    # Drainage Area (DA)
    drainage_area = closest_flowline_feature.get('DvDASqK', np.nan) if closest_flowline_feature is not None else np.nan

    # Flood Depth Difference
    flood_depth_diff = compute_flood_depth_difference(fd_10_dataset, fd_100_dataset, closest_feature_geom)

    return closest_feature_distance, river_elev, err, drainage_area, flood_depth_diff

def compute_flood_depth_difference(fd_10_dataset, fd_100_dataset, closest_feature_geom):
    """Compute flood depth difference from 100-year and 1000-year flood datasets."""
    if closest_feature_geom is None:
        return np.nan

    fd_10_mean = mask_and_mean(fd_10_dataset, [closest_feature_geom.geometry])
    fd_100_mean = mask_and_mean(fd_100_dataset, [closest_feature_geom.geometry])

    if fd_100_mean is not None:
        if fd_10_mean is not None:
            return abs(fd_100_mean - fd_10_mean) 
        else:
            return fd_100_mean 
    else:
        return 0

def mask_and_mean(dataset, geometries, nodata=-9999):
    """Mask the dataset by geometries and return the mean of valid data."""
    out, _ = mask(dataset, geometries, crop=True)
    data = out[0]
    data = data[data != dataset.nodata]
    return data.mean() if data.size > 0 else None


