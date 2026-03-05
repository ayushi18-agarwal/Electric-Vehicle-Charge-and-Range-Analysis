#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 19:59:58 2026

@author: ayushiagarwal
"""

import pandas as pd
import numpy as np

# -----------------------------
# 1 Load dataset
# -----------------------------
df = pd.read_csv("merged.csv")

print("Original Shape:", df.shape)

# -----------------------------
# 2 Standardize column names
# -----------------------------
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# -----------------------------
# 3 Remove duplicate rows
# -----------------------------
df = df.drop_duplicates()

# -----------------------------
# 4 Replace invalid values
# -----------------------------
df.replace(["-", "N/A", "na", "null", ""], np.nan, inplace=True)

# -----------------------------
# 5 Remove units and extract numbers
# -----------------------------
def extract_number(col):
    return col.astype(str).str.extract(r'(\d+\.?\d*)')[0].astype(float)

possible_numeric = [
    "acceleration",
    "topspeed",
    "range",
    "efficiency",
    "battery_capacity",
    "fastcharge_speed"
]

for col in possible_numeric:
    if col in df.columns:
        df[col] = extract_number(df[col])

# -----------------------------
# 6 Clean categorical text
# -----------------------------
for col in df.select_dtypes(include="object"):
    df[col] = df[col].str.strip().str.lower()

# -----------------------------
# 7 Identify numeric and categorical columns
# -----------------------------
num_cols = df.select_dtypes(include=np.number).columns
cat_cols = df.select_dtypes(include="object").columns

# -----------------------------
# 8 Handle missing values
# -----------------------------
# Numeric → median
for col in num_cols:
    df[col] = df[col].fillna(df[col].median())

# Categorical → mode
for col in cat_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# -----------------------------
# 9 Remove columns with too many missing values
# -----------------------------
df = df.dropna(thresh=len(df)*0.6, axis=1)

# -----------------------------
# 10 Remove constant columns
# -----------------------------
df = df.loc[:, df.nunique() > 1]

# -----------------------------
# 11 Handle outliers (cap instead of delete)
# -----------------------------
for col in num_cols:

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    df[col] = np.where(df[col] < lower, lower, df[col])
    df[col] = np.where(df[col] > upper, upper, df[col])

# -----------------------------
# 12 Feature Engineering
# -----------------------------
if "range" in df.columns and "battery_capacity" in df.columns:
    df["range_per_kwh"] = df["range"] / df["battery_capacity"]

if "topspeed" in df.columns:
    df["speed_category"] = pd.cut(
        df["topspeed"],
        bins=[0,150,200,250,400],
        labels=["low","medium","high","super"]
    )

if "acceleration" in df.columns:
    df["acceleration_class"] = pd.cut(
        df["acceleration"],
        bins=[0,4,7,12],
        labels=["sports","standard","slow"]
    )

# -----------------------------
# 13 Normalize numeric values
# -----------------------------
for col in num_cols:
    df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

# -----------------------------
# 14 Reset index
# -----------------------------
df.reset_index(drop=True, inplace=True)

print("Cleaned Shape:", df.shape)

# -----------------------------
# 15 Save cleaned dataset
# -----------------------------
df.to_csv("ev_dataset_clean_final.csv", index=False)

print("Clean dataset saved successfully!")