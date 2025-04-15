#!/bin/bash

# Ensure environment is activated before running:
# conda activate env_name
cd "$(dirname "$0")"/..  # Navigate to project root relative to this script
python scripts/main.py \
    --years 12 22 32 42 52 \
    --plans FWOA FWMP \
    --scenarios Higher Lower \
    --structure_csv data/structure_csv/mp23_pdd_clara_structure_info_costs_2024_06_18.csv \
    --column_setup full \
    --insurance 32 \
    --parallel
