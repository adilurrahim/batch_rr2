import pandas as pd
import numpy as np
from tqdm.auto import tqdm

def assign_insurance(structure_df, insurance_df, n_iterations=10):
    """
    Assigns insurance based on majority voting across multiple random seeds.
    """

    insurance_df.columns = insurance_df.columns.str.strip()
    insurance_df = insurance_df.rename(columns={
        'SFHZipCode': 'zip_sfh', 'SFHCounts': 'count_sfh',
        'AllZipCode': 'zip_all', 'AllCounts': 'count_all'
    })

    # Ensure ZIP codes are string formatted for consistency
    #structure_df['zipcode'] = structure_df['zipcode'].astype(str).str.zfill(5)
    structure_df['zipcode'] = structure_df['zipcode'].astype(str).str.split('.').str[0].str.zfill(5)
    insurance_df['zip_sfh'] = insurance_df['zip_sfh'].astype(str).str.zfill(5)
    insurance_df['zip_all'] = insurance_df['zip_all'].astype(str).str.zfill(5)

    insurance_df[['count_sfh', 'count_all']] = insurance_df[['count_sfh', 'count_all']].fillna(0)
    insurance_df[['count_sfh', 'count_all']] = insurance_df[['count_sfh', 'count_all']].astype(int)

    # Add default columns
    structure_df["insurance_votes"] = 0

    # Loop over 
    for i in tqdm(range(n_iterations), desc=f"Running insurance assignment by majority voting)"):
        temp_df = structure_df.copy()
        temp_df["has_insurance"] = 0  # default to no
        
        for zip_code in temp_df['zipcode'].unique():
            sfh_count = insurance_df[insurance_df['zip_sfh'] == zip_code]
            all_row = insurance_df[insurance_df['zip_all'] == zip_code]
    
            sfh_count = int(sfh_count['count_sfh'].values[0]) if not sfh_count.empty else 0
            all_count = int(all_row['count_all'].values[0]) if not all_row.empty else 0
            non_sfh_count = max(0, all_count - sfh_count)
    
            # Filter buildings in that ZIP
            zip_buildings = temp_df[temp_df['zipcode'] == zip_code]
            if zip_buildings.empty:
                continue
      
            res1_buildings = zip_buildings[zip_buildings['gbs_code'] == "RES1"]
            other_buildings = zip_buildings[zip_buildings['gbs_code'] != "RES1"]
    
            # Sample RES1 for SFH insurance
            res1_sample = res1_buildings.sample(min(sfh_count, len(res1_buildings)), random_state=i)
            temp_df.loc[res1_sample.index, 'has_insurance'] = 1
    
            # Sample remaining for others
            other_sample = other_buildings.sample(min(non_sfh_count, len(other_buildings)), random_state=i)
            temp_df.loc[other_sample.index, 'has_insurance'] = 1
        
        structure_df["insurance_votes"] += temp_df["has_insurance"]
    
    structure_df["has_insurance"] = (structure_df["insurance_votes"] >= (n_iterations // 2 + 1)).astype(int)

    # Any structure without ZIP code automatically stays "No"
    return structure_df

