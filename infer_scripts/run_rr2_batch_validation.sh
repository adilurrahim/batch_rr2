#!/bin/bash

# Ensure environment is activated before running:
# conda activate env_name

cd "$(dirname "$0")"/..  # Navigate to project root relative to this script

python scripts/main_Validate.py \
    --years 2 \
    --plans FWOA \
    --scenarios Lower \
    --structure_csv data/structure_csv/validate_60.csv

