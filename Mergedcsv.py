#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 19:47:15 2026

@author: ayushiagarwal
"""

import pandas as pd

# List of CSV files
csv_files = ['Cheapestelectriccars-EVDatabase.csv', 'electric_vehicle_charging_station_list.csv', 'ElectricCarData_Clean.csv', 'EVIndia.csv']

# Read and concatenate all CSVs
merged_df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

# Save to a new CSV
merged_df.to_csv('merged.csv', index=False)

print("All CSV files merged into merged.csv")
