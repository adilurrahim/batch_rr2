import argparse
import os
import pandas as pd
from tqdm.auto import tqdm
import logging

from rr2_premium_functions import *
from geographic_attributes import extract_geographic_attributes
from table_loader import load_rr2_tables

def run_batch_pipeline(args):
    os.makedirs(args.output_dir, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    years = args.years
    plans = args.plans
    scenarios = args.scenarios

    # Load structure CSV
    logging.info(f"Loading structure data from: {args.structure_csv}")
    structure_df = pd.read_csv(args.structure_csv)
    
    # Load occupancy mapping table
    if args.occupancy_map:
       logging.info(f"Loading occupancy mapping table from: {args.occupancy_map}")
       mapping_df = pd.read_csv(args.occupancy_map)
       mapping_df.columns = mapping_df.columns.str.strip()
       occupancy_to_type = dict(zip(mapping_df["OccupancyTypeName"], mapping_df["TypeofUse"]))
       structure_df["TypeofUse"] = structure_df["gbs_code"].map(occupancy_to_type)
    
    foundationType_mapping = {
                            0: "Elevated with Enclosure, Post, Pile, or Pier",
                            1: "Slab",
                            2: "Elevated with Enclosure, Not Post, Pile, or Pier",
                            3: "Crawlspace",  
                            None: "Slab"
                        }
    structure_df["FoundationType"] = structure_df["foundation_type(0=pier;1=slab;2=mobilehome;3=other;null=slab)"].map(foundationType_mapping).fillna("Slab")

    # Foundation Design mapping based on FoundationType
    foundationDesign_mapping = {
                                "Elevated with Enclosure, Post, Pile, or Pier": "Open, Obstruction",
                                "Elevated without Enclosure, Post, Pile, or Pier": "Open, No Obstruction",
                                "Elevated with Enclosure, Not Post, Pile, or Pier": "Open, Obstruction",
                                "Crawlspace": "Open, Obstruction",
                                "Slab": "Closed, Wall",
                                "Basement": "Closed, Wall"
                                }  
    
    # Filter if insurance option is on
    if args.insurance:
        if 'has_insurance' not in structure_df.columns:
            raise ValueError("The structure CSV must contain an 'has_insurance' column when --insurance flag is used.")
        structure_df = structure_df[structure_df['has_insurance'].astype(str).str.lower().isin(["yes","Yes","1","true","True"])]
        logging.info(f"Filtered structures to {len(structure_df)} insured entries")                             
    # Load all required RR2 tables
    logging.info("Loading FEMA RR2 Rating Factors tables...")
    tables_L, tables_NL, tables_BA, tables_PA = load_rr2_tables()

    for year in years:
        for plan in plans:
            for scenario in scenarios:
                logging.info(f"Running: Year={year}, Plan={plan}, Scenario={scenario}")

                # Extract geographic attributes
                logging.info("Extracting geographic attributes...")
                geographic_df = extract_geographic_attributes(
                    structure_df.copy(),
                    year=year,
                    plan=plan,
                    scenario=scenario,
                    base_path=args.data_path,
                )
                logging.info(f"Geographic attributes extracted for {len(geographic_df)} structures")

                # Merge back with structure file
                df = structure_df.merge(geographic_df, on="structure_id")

                # Estimate premiums
                rr2_premiums = []
                for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Estimating premiums {year}-{plan}-{scenario}"):
                    inputs = {}
                    # Geographic Attributes
                    inputs['DTR'] = row['DTR'] 
                    inputs['ERR'] = row['ERR'] * 3.2808399
                    inputs['DrainageArea'] = row['DrainageArea']
                    inputs['RiverClass'] = row['RiverClass']
                    inputs['DTC'] = row['DTC']
                    inputs['StructRelElev'] = row['StructRelElev'] * 3.2808399
                    inputs['Elevation'] = row['Elevation'] * 3.2808399
                    inputs['County'] = row['County'] + " Parish"
                    inputs['State'] = "LA"
                    inputs['State(Long)'] = "Louisiana"

                    inputs['HUC12'] = int(row['HUC12']) if isinstance(row['HUC12'], str) else row['HUC12']
                    inputs['CRS'] = min(row['CRS']) if row['CRS'] else 10

                    if row['LeveeSystemId']:
                        for levee in row['LeveeSystemId']:
                            if levee in tables_L["Levee_IF"]['Levee System ID'].values:
                                inputs['LeveeSystemId'] = levee
                    else:
                        inputs['LeveeSystemId'] = pd.NA

                    ### Building Attributes
                    inputs['PrimaryResidence'] = "Yes"
                    
                    ##
                    if row["imputed_num_stories"]!=-99:
                        inputs["FloorofInterest"] = row["imputed_num_stories"]
                    elif row["num_stories"]:
                        inputs["FloorofInterest"] = row["num_stories"]
                    else:
                        inputs["FloorofInterest"] = 1
                    
                    ##
                    typeofUse = row["TypeofUse"]    
                    if "Single-Family" in typeofUse:
                        inputs["TypeofUse"] = "Single-Family Home - Frame"
                        inputs["SingleFamilyHomeIndicator"] = "Yes"
                        inputs["CondoUnitOwnerIndicator"] = "No"
                    
                    elif "Two to Four Family" in typeofUse:
                        inputs["TypeofUse"] = "Two to Four Family Building - Frame"
                        inputs["SingleFamilyHomeIndicator"] = "Yes"
                        inputs["Condo Unit Owner Indicator"] = "No"
                    
                    else:
                        inputs["TypeofUse"] = row["TypeofUse"]
                        inputs["SingleFamilyHomeIndicator"] = "No"
                        inputs["CondoUnitOwnerIndicator"] = "No"
                    
                    ##
                    inputs["FoundationType"] = row["FoundationType"]                    
                    inputs["FoundationDesign"] = foundationDesign_mapping.get(inputs["FoundationType"])

                    ##
                    inputs['FloodVents'] = "No"
                    inputs['ffh'] = row['imputed_foundation_ht']
                    inputs['BuildingValue'] = row['structure_value']
                    inputs['ContentsValue'] = row['contents_value']

                    # Policy Attributes
                    inputs['coverageA'] = 250000
                    inputs['coverageC'] = 100000
                    inputs['deductibleA'] = 5000
                    inputs['deductibleC'] = 5000
                    inputs['PriorClaim'] = 0
                    if pd.isna(inputs['LeveeSystemId']):
                        premium = rr2NL(inputs, tables_NL, tables_BA, tables_PA)
                    else:
                        premium = rr2Levee(inputs, tables_L, tables_BA, tables_PA)

                    premium.insert(0, row['structure_id'])
                    rr2_premiums.append(premium)

                # Save outputs
                out_df = pd.DataFrame(rr2_premiums, columns=[
                    "structure_id", "Building Premium", "Contents Premium",
                    "Increased Cost of Compliance Premium", "Mitigation Discount",
                    "Community Rating Systems Discount", "Full-Risk Premium"])

                if args.column_setup.lower() == "full":
                    out_df = pd.merge(geographic_df, out_df, on="structure_id")

                filename = f"rr2_{year}_{plan}_{scenario}.csv"
                out_df.to_csv(os.path.join(args.output_dir, filename), index=False)
                logging.info(f"Saved: {filename}")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--years", nargs="+", type=int, required=True)
    parser.add_argument("--plans", nargs="+", required=True)
    parser.add_argument("--scenarios", nargs="+", required=True)
    parser.add_argument("--structure_csv", type=str, default="data/structure_csv/mp23_pdd_clara.structure_info_costs_2024.06.18.csv")
    parser.add_argument("--data_path", type=str, default="data/ProcessedData")
    parser.add_argument("--tables_dir", type=str, default="scripts/rr2_tables")
    parser.add_argument("--output_dir", type=str, default="output/")
    parser.add_argument("--column_setup", choices=["premium", "full"], default="premium")
    parser.add_argument("--insurance", action="store_true", help= "Only compute premiums for insured structures")
    parser.add_argument("--occupancy_map", type=str, default="data/OccupancyMapping/OccupancytoTypeofUseMapping.csv", help="Path to occupancy mapping csv file")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    run_batch_pipeline(args)