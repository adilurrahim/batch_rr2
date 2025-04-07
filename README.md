# Batch RR2 Model Pipeline

This repository contains the **batch_rr2** model pipeline to estimate Risk Rating 2.0 (RR2) flood insurance premiums using CPRA Coastal Master Plan 2023. The code extracts geographic attributes from structure coordinates and computes RR2 premiums.

---

## 📦 Installation

### Method 1: With pip (future support planned)
```bash
pip install batch_rr2
```

### Method 2: From the source (recommended)
```bash
git clone https://github.com/adilurrahim/batch_rr2.git
cd batch_rr2
conda create -n batch_rr2 python=3.10
conda activate batch_rr2
pip install -r requirements.txt
```

---

## Getting Started

### Step 1: Input Directory Structure
```
data/
├── structure_csv/
│   └── mp23_pdd_clara_structure_info_costs_2024_06_18.csv
├── OccupancyMapping/
│   └── OccupancytoTypeofUseMapping.csv
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

### Step 2: Run the Pipeline

```bash
python scripts/main.py \
    --years 2 12 22 32 42 52 \
    --plans FWOA FWMP \
    --scenarios Higher Lower \
    --structure_csv data/structure_csv/mp23_pdd_clara.structure_info_costs_2024.06.18.csv \
    --data_path data/ProcessedData \
    --tables_dir scripts/rr2_tables \
    --column_setup full \
    --insurance \
    --output_dir output/
```

> You can control which buildings to calculate insurance premiums for using the `--insurance` flag. If set, premiums will be calculated only for rows with has_insurance = `Yes` or `1` or `True`.

---

## Customization via CLI

| Flag | Description |
|------|-------------|
| `--years` | List of years (e.g., `2 22 32`) |
| `--plans` | Scenario plans (e.g., `FWOA FWMP`) |
| `--scenarios` | Scenarios (e.g., `Higher Lower`) |
| `--structure_csv` | Path to structure CSV |
| `--data_path` | Root directory for all processed GIS and raster data |
| `--tables_dir` | Root directory for all FEMA rating factor tables |
| `--output_dir` | Path to save the results |
| `--column_setup` | Choose between `premium` or `full` columns |
| `--insurance` | Flag to calculate premiums for insured buildings only |
| `--occupancy_map` | Optional occupancy mapping CSV |

---

## Output Columns

### Column Setup: `premium`
- structure_id
- Building Premium
- Contents Premium
- Increased Cost of Compliance Premium
- Mitigation Discount
- Community Rating Systems Discount
- Full-Risk Premium

### Column Setup: `full`
In addition to the above:
- County
- HUC12
- CRS
- LeveeSystemId
- Elevation
- StructRelElev
- DTR
- ElevRiver
- ERR
- DrainageArea
- RiverClass
- DTC

---

## 📁 Project Structure
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

## Python Requirements
```
Python 3.10+

# Install packages
pip install -r requirements.txt
```

---

## 📧 Questions?
Open an issue or contact:
**Md Adilur Rahim**  
mrahim@agcenter.lsu.edu  
LSU AgCenter
