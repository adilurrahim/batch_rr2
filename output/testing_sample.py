import os
os.chdir(r"C:\Users\mrahim\Downloads\CPRA\Scripts\Github")

os.chdir(r"C:\Users\mrahim\Downloads\CPRA\Scripts\Github\scripts")

from types import SimpleNamespace
args = SimpleNamespace(
    years=[2],
    plans=["FWOA"],
    scenarios=["Lower"],
    occupancy_map = "data/OccupancyMapping/OccupancytoTypeofUseMapping.csv",
    structure_csv = "data/structure_csv/validate_60.csv",
    data_path = "C:/Users/mrahim/Downloads/CPRA/Scripts/Github/data/ProcessedData",
    insurance = 25,
    existing_geo = "output/geo_2_FWOA_Lower.csv",
    output_dir = "output"
)

import time
start = time.time()
!python scripts/main.py --years 2 --plans FWOA --scenarios Lower --structure_csv data/structure_csv/mp23_pdd_clara_structure_info_costs_2024_06_18.csv --column_setup full --insurance 25 --existing_geo --parallel
time.time()-start

#####################

import pandas as pd
insurance_df = pd.read_csv("data/InsurancePolicyDistribution/FEMAPolicyCounts/fema_risk-rating-zip-breakdown_2021.csv")
structure_df = pd.read_csv("data/structure_csv/mp23_pdd_clara_structure_info_costs_2024_06_18.csv")

other_sample = structure_df.sample(1000)
other_sample.to_csv("data/structure_csv/sample_1000.csv",index=False)


geographic_df =  pd.read_csv("output/rr2_GA_2_FWOA_Lower.csv")


floor_int = tables_BA["floorInterest"]

floor_int = floor_int[(floor_int['Single & 2-4 Family Home Indicator']==inputs['SingleFamilyHomeIndicator'])
                      & (floor_int['Condo Unit Owner Indicator']==inputs['CondoUnitOwnerIndicator'])
                      & (floor_int['Floors of Interest']==str(int(inputs['FloorofInterest'])))]
