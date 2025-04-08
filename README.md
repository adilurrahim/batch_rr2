## Batch RR2 Model Pipeline

This repository contains the **batch_rr2** model pipeline to estimate Risk Rating 2.0 (RR2) flood insurance premiums using CPRA Coastal Master Plan 2023. The code extracts geographic attributes from structure coordinates and computes RR2 premiums.

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
├── data/                     	# Input structure CSVs, occupancy maps, processed data
├── output/                   	# Output folder for premium calculations
├── rr2_tables/               	# FEMA RR2 tables (CSV format)
├── scripts/                  	# Main logic and functions
│   ├── geographic_attributes.py
│   ├── helper_functions.py
│   ├── main.py
│   ├── rr2_premium_functions.py
│   └── table_loader.py
├── infer_scripts/            	# Bash scripts to run example jobs
├── requirements.txt
├── README.md
```

---

#### Step 2: Run the Pipeline

```bash
python scripts/main.py \
    --years 2 12 22 32 42 52 \
    --plans FWOA FWMP \
    --scenarios Higher Lower \
    --structure_csv data/structure_csv/mp23_pdd_clara_structure_info_costs_2024_06_18.csv \
    --data_path data/ProcessedData \
    --tables_dir scripts/rr2_tables \
    --existing_geo \
    --output_dir output \
    --column_setup full \
    --insurance 25 \
    --occupancy_map data/OccupancyMapping/OccupancytoTypeofUseMapping.csv \
    --parallel
```

> Use the --insurance flag to restrict calculations to insured structures only. If a number is provided (e.g., --insurance 25), it controls the number of iterations for stochastic assignment. If used without a value (i.e., --insurance), the default is 10 iterations.

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

#### --column_setup premium
- structure_id
- Building Premium
- Contents Premium
- Increased Cost of Compliance Premium
- Mitigation Discount
- Community Rating Systems Discount
- Full-Risk Premium

#### --column_setup full (adds geographic info)
In addition to the above:
- County, HUC12, CRS, LeveeSystemId, Elevation
- StructRelElev, DTR, ElevRiver, ERR, DrainageArea, RiverClass, DTC

---

#### Python Requirements
```
Python 3.10+

# Install dependencies:
pip install -r requirements.txt
```

---
