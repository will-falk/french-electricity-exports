"""
Run locally to fetch fresh data from ENTSOE API and save to data/*.parquet.
Commit the resulting files so Render can load them without API access.

Usage:
    /Users/clarence/miniconda3/envs/french-electricity-exports/bin/python refresh_data.py
"""
import os
import data_extraction_processing as dep

os.makedirs('data', exist_ok=True)

for period, df in dep.fr_final_frames_by_period.items():
    df.to_parquet(f'data/fr_{period}.parquet')
    print(f"Saved data/fr_{period}.parquet ({len(df)} rows, {len(df.columns)} zones)")

for period, df in dep.no_final_frames_by_period.items():
    df.to_parquet(f'data/no_{period}.parquet')
    print(f"Saved data/no_{period}.parquet ({len(df)} rows, {len(df.columns)} zones)")

print("Done. Commit the data/ directory and push to redeploy.")
