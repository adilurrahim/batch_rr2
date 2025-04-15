import geopandas as gpd
import pandas as pd

def extract_zip_codes_from_shapefile(
    structure_csv_path,
    zip_shapefile_path,
    output_path,
    lat_col='lat',
    lon_col='lon',
    structure_crs="EPSG:4326",
    zip_crs="EPSG:4326",
    save = False
):
    """
    Assigns ZIP codes to structure points using spatial join with ZCTA shapefile.
    """
    structure_df = pd.read_csv(structure_csv_path)
    structure_gdf = gpd.GeoDataFrame(
        structure_df,
        geometry=gpd.points_from_xy(structure_df[lon_col], structure_df[lat_col]),
        crs=structure_crs
    )

    zip_gdf = gpd.read_file(zip_shapefile_path).to_crs(zip_crs)

    structure_with_zip = gpd.sjoin(
        structure_gdf,
        zip_gdf[["ZCTA5CE20", "geometry"]],
        how="left",
        predicate="within"
    )

    structure_with_zip = structure_with_zip.rename(columns={"ZCTA5CE20": "zipcode"})
    structure_with_zip["zipcode"] = structure_with_zip["zipcode"].fillna("00000").astype(str).str.zfill(5)
    structure_with_zip = structure_with_zip.drop(columns=["geometry", "index_right"])
    if save:
        structure_with_zip.to_csv(output_path, index=False)
        print(f"Structure ZIP codes extracted and saved to: {output_path}")
    
    return structure_with_zip
    