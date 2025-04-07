import os
import pandas as pd

def load_rr2_tables(base_path="rr2_tables"):
    tables_L = {}
    tables_NL = {}
    tables_BA = {}
    tables_PA = {}

    # Levee-based tables
    tables_L["BaseRates"] = pd.read_csv(os.path.join(base_path, 'BaseRates - L.csv'))
    tables_L["DTR"] = pd.read_csv(os.path.join(base_path, 'DTR - L.csv'))
    tables_L["ERR"] = pd.read_csv(os.path.join(base_path, 'ElevRelRiver - L.csv'))
    tables_L["DrainageArea"] = pd.read_csv(os.path.join(base_path, 'DrainageArea - L.csv'))
    tables_L["SructRelElev"] = pd.read_csv(os.path.join(base_path, 'StructRelElev - L.csv'))
    tables_L["DTC_CE"] = pd.read_csv(os.path.join(base_path, 'DTC - CE - L.csv'))
    tables_L["DTC_SS"] = pd.read_csv(os.path.join(base_path, 'DTC - SS - L.csv'))
    tables_L["Elev_IFSS"] = pd.read_csv(os.path.join(base_path, 'Elevation - IFSS - L.csv'))
    tables_L["Levee_IF"] = pd.read_csv(os.path.join(base_path, 'Levee Quality-IF.csv'))
    tables_L["Levee_SS"] = pd.read_csv(os.path.join(base_path, 'Levee Quality-SS.csv'))
    tables_L["Territory_IFSS"] = pd.read_csv(os.path.join(base_path, 'Territory - IFSS - L.csv'))

    # Non-levee-based tables
    tables_NL["BaseRates"] = pd.read_csv(os.path.join(base_path, 'BaseRates - NL.csv'))
    tables_NL["DTR"] = pd.read_csv(os.path.join(base_path, 'DTR - NL.csv'))
    tables_NL["ERR"] = pd.read_csv(os.path.join(base_path, 'ElevRelRiver - NL - Seg 1-4.csv'))
    tables_NL["DrainageArea"] = pd.read_csv(os.path.join(base_path, 'DrainageArea - NL.csv'))
    tables_NL["SructRelElev"] = pd.read_csv(os.path.join(base_path, 'StructRelElev - NL.csv'))
    tables_NL["DTC_CE"] = pd.read_csv(os.path.join(base_path, 'DTC - CE - NL.csv'))
    tables_NL["DTC"] = pd.read_csv(os.path.join(base_path, 'DTC - Non-BI - NL.csv'))
    tables_NL["Elev"] = pd.read_csv(os.path.join(base_path, 'Elevation - Non-BI - NL.csv'))
    tables_NL["Territory"] = pd.read_csv(os.path.join(base_path, 'Territory - Non-BI - NL.csv'))

    # Building Attributes tables
    tables_BA["typeUse"] = pd.read_csv(os.path.join(base_path, 'Type of Use.csv'))
    tables_BA["floorInterest"] = pd.read_csv(os.path.join(base_path, 'Floors of Interest.csv'))
    tables_BA["foundationType"] = pd.read_csv(os.path.join(base_path, 'Foundation Type.csv'))
    tables_BA["firstfloorHeight"] = pd.read_csv(os.path.join(base_path, 'First Floor Height.csv'))
    tables_BA["buildingValue"] = pd.read_csv(os.path.join(base_path, 'Building Value.csv'))
    tables_BA["contentsValue"] = pd.read_csv(os.path.join(base_path, 'Contents Value.csv'))
    tables_BA["RCV_Caps"] = pd.read_csv(os.path.join(base_path, 'RCV Caps.csv'))

    # Policy Attributes tables
    tables_PA["deductible_limit_coverage_A"] = pd.read_csv(os.path.join(base_path, 'Deductible Limit ITV Cov A.csv'))
    tables_PA["deductible_limit_coverage_C"] = pd.read_csv(os.path.join(base_path, 'Deductible Limit ITV Cov C.csv'))
    tables_PA["deductible_coverage_A"] = pd.read_csv(os.path.join(base_path, 'Deductible ITV Cov A.csv'))
    tables_PA["deductible_coverage_C"] = pd.read_csv(os.path.join(base_path, 'Deductible ITV Cov C.csv'))
    tables_PA["concRisk"] = pd.read_csv(os.path.join(base_path, 'Concentration Risk.csv'))
    tables_PA["concriskMapping"] = pd.read_csv(os.path.join(base_path, 'Concentration Risk Mapping.csv'))

    return tables_L, tables_NL, tables_BA, tables_PA