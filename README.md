## Batch RR2 Model Pipeline

This repository contains the **batch_rr2** model pipeline to estimate Risk Rating 2.0 (RR2) flood insurance premiums using CPRA Coastal Master Plan 2023. This repository contains the batch_rr2 model pipeline to estimate FEMA’s Risk Rating 2.0 (RR2.0) flood insurance premiums at the structure level under multiple Coastal Master Plan scenarios. 


---

### 📦 Installation

#### Method 1: With pip (future support planned)
```bash
pip install batch_rr2
```

#### Method 2: From the source (recommended)
```bash
git clone https://github.com/adilurrahim/batch_rr2.git
cd batch_rr2
conda create -n batch_rr2 python=3.10
conda activate batch_rr2
pip install -r requirements.txt
```

---

### Getting Started

#### Step 1: Project Structure
```
data/
├── structure_csv/
│   └── mp23_pdd_clara_structure_info_costs_2024_06_18.csv
├── OccupancyMapping/
│   └── OccupancytoTypeofUseMapping.csv
├── InsurancePolicyDistribution/
│   ├── ZipCodeData/
│   │   └── tl_2021_us_zcta520.shp
│   └── FEMAPolicyCounts/
│       └── fema_risk-rating-zip-breakdown_2021.csv
├── ProcessedData/
│   └── CommonData/
│       ├── County/
│       ├── CRS/
│       ├── FlowLine/
│       ├── RiverPolygon/
│       └── HUC12/
│   └── ScenarioSpecificData/
│       └── 2/
│           └── FWOA/
│               └── Lower/
│                   ├── CoastLine/
│                   ├── Elevation/
│                   ├── FloodDepth/
│                   └── Levee/
```

---

#### Step 2: Run the Pipeline

```bash
python scripts/main.py \
    --years 12 22 32 42 52 \
    --plans FWOA FWMP \
    --scenarios Higher Lower \
    --structure_csv data/structure_csv/mp23_pdd_clara_structure_info_costs_2024_06_18.csv \
    --data_path data/ProcessedData \
    --tables_dir scripts/rr2_tables \
    --existing_geo \
    --output_dir output \
    --column_setup full \
    --insurance 32 \
    --occupancy_map data/OccupancyMapping/OccupancytoTypeofUseMapping.csv \
    --parallel
```

> Use the --insurance flag to restrict calculations to insured structures only. If a number is provided (e.g., --insurance 32), it controls the number of iterations for stochastic assignment. If used without a value (i.e., --insurance), the default is 10 iterations.
> Add --parallel for faster geographic attribute extraction. 
> Add --existing_geo to use precomputed geospatial attributes (if any).
> Example inference scripts to batch-run premium calculations across multiple simulations using predefined bash commands are stored in infer_scripts folder.
---

#### Customization via CLI

| Flag | Description |
|------|-------------|
| `--years`         | List of years (`2 12 22 32 42 52`) |
| `--plans`         | Scenario plans ( `FWOA FWMP`) |
| `--scenarios`     | Scenarios (`Higher Lower`) |
| `--structure_csv` | Path to structure CSV |
| `--data_path`     | Root directory for all processed GIS and raster data |
| `--tables_dir`    | Root directory for all FEMA rating factor tables |
| `--existing_geo`  | Path to existing geographic_df CSV file to skip extraction |
| `--output_dir`    | Path to save the results |
| `--column_setup`  | Choose between `premium` (default) or `full` columns |
| `--insurance`     | Flag to calculate premiums for insured buildings only, number of iterations for insurance flag assignment  |
| `--occupancy_map` | Optional: Path to occupancy-to-TypeOfUse mapping CSV |
| `--parallel`      | Optional: enable parallel processing of geographic attributes extraction |

---

#### Output Files
- `rr2_geo_<year>_<plan>_<scenario>.csv`: Geographic attributes for each structure
- `rr2_<year>_<plan>_<scenario>.csv`: RR2 premium results

---

#### Output Columns

##### --column_setup premium
- structure_id
- Building Premium
- Contents Premium
- Increased Cost of Compliance Premium
- Mitigation Discount
- Community Rating Systems Discount
- Full-Risk Premium

##### --column_setup full (adds geographic info)
In addition to the above:
- County, HUC12, CRS, LeveeSystemId, Elevation
- StructRelElev, DTR, ElevRiver, ERR, DrainageArea, RiverClass, DTC

---

#### 📁 Project Structure
```
├── data/                     	# Input structure CSVs, occupancy maps, processed data
├── output/                   	# Output folder for premium calculations
├── rr2_tables/               	# FEMA RR2 tables (CSV format)
├── scripts/                  	# Main logic and functions
│   ├── helper_functions.py
│   ├── geographic_attributes_chunk.py   #for parallel processing
│   ├── geographic_attributes.py
│   ├── rr2_premium_functions.py
│   ├── insurance_utils.py
│   ├── table_loader.py
│   └── main.py
├── infer_scripts/            	 # Bash scripts to run example jobs
├── requirements.txt
├── README.md
```

---

#### Python Requirements
```
Python 3.10+

# Install dependencies:
pip install -r requirements.txt
```

---
#### License

---
