#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 20:36:26 2026

@author: ayushiagarwal
"""

# ===============================================
# EV DASHBOARD DATA PREPROCESSING SCRIPT
# Supports:
# Scenario 1 - Charging Pattern Analysis
# Scenario 2 - Battery Performance Analysis
# Scenario 3 - EV Model Comparison
# ===============================================

import pandas as pd
import numpy as np

# -------------------------------
# STEP 1: LOAD DATASET
# -------------------------------
df = pd.read_csv("ev_battery_charging_data.csv")

print("Original Shape:", df.shape)
print("\nMissing Values:\n", df.isnull().sum())

# -------------------------------
# STEP 2: DATA CLEANING
# -------------------------------

# Remove duplicates
df.drop_duplicates(inplace=True)

# Fill numeric missing values with median
numeric_cols = df.select_dtypes(include=np.number).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# Fill categorical missing values with mode
categorical_cols = df.select_dtypes(include='object').columns
for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# Remove unrealistic SOC values
df = df[(df["SOC (%)"] >= 0) & (df["SOC (%)"] <= 100)]

# Remove unrealistic battery temperature
df = df[(df["Battery Temp (°C)"] > 0) & (df["Battery Temp (°C)"] < 70)]

print("\nShape After Cleaning:", df.shape)

# -------------------------------
# STEP 3: ADD NEW COLUMNS
# -------------------------------

# 1️⃣ Charging Date
df["Charging Date"] = pd.to_datetime("2025-01-01") + pd.to_timedelta(
    np.random.randint(0, 180, size=len(df)), unit='D'
)

# 2️⃣ Charging Start Hour
df["Charging Start Hour"] = np.random.randint(0, 24, size=len(df))

# 3️⃣ City / Location
cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai"]
df["City"] = np.random.choice(cities, size=len(df))

# 4️⃣ Energy Consumed (kWh)
df["Energy (kWh)"] = (
    df["Voltage (V)"] * df["Current (A)"] * df["Charging Duration (min)"] / 1000
)

# 5️⃣ Battery Capacity (kWh) based on EV Model
capacity_map = {
    "Model A": 40,
    "Model B": 60,
    "Model C": 75
}

df["Battery Capacity (kWh)"] = df["EV Model"].map(capacity_map)

# 6️⃣ Estimated Driving Range (km)
df["Estimated Range (km)"] = (
    df["Battery Capacity (kWh)"] * df["Efficiency (%)"] / 100 * 5
)

# 7️⃣ Battery Health Index
df["Battery Health (%)"] = 100 - df["Degradation Rate (%)"]

# 8️⃣ Charging Cost (₹)
electricity_cost = 8  # ₹8 per kWh (India example)
df["Charging Cost (₹)"] = df["Energy (kWh)"] * electricity_cost

# -------------------------------
# STEP 4: FEATURE ENGINEERING
# -------------------------------

# Load Category
df["Load Category"] = pd.cut(
    df["Energy (kWh)"],
    bins=[0, 20, 50, 100],
    labels=["Low", "Medium", "High"]
)

# Efficiency Category
df["Efficiency Category"] = pd.cut(
    df["Efficiency (%)"],
    bins=[0, 70, 85, 100],
    labels=["Low", "Moderate", "High"]
)

# Stress Index
df["Stress Index"] = df["Battery Temp (°C)"] * df["Charging Duration (min)"]

# Efficiency Loss per Cycle
df["Efficiency Loss per Cycle"] = (
    df["Degradation Rate (%)"] / (df["Charging Cycles"] + 1)
)

# -------------------------------
# STEP 5: RENAME COLUMNS (Tableau Friendly)
# -------------------------------

df.columns = df.columns.str.replace(" ", "_")
df.columns = df.columns.str.replace("(", "", regex=False)
df.columns = df.columns.str.replace(")", "", regex=False)
df.columns = df.columns.str.replace("%", "Percent", regex=False)
df.columns = df.columns.str.replace("°", "", regex=False)
df.columns = df.columns.str.replace("₹", "INR", regex=False)

# -------------------------------
# STEP 6: SAVE FINAL DATASET
# -------------------------------

df.to_csv("ev_dashboard_ready_dataset.csv", index=False)

print("\n✅ Data Processing Complete!")
print("Final Shape:", df.shape)
print("Saved as: ev_dashboard_ready_dataset.csv")