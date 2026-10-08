from pathlib import Path
import pandas as pd

RAW_FILE = Path("data/raw/DataCoSupplyChainDataset.csv")

if not RAW_FILE.exists():
    raise FileNotFoundError(f"File not found: {RAW_FILE}")

df = pd.read_csv(RAW_FILE, encoding="latin1")

print("=" * 70)
print("DATASET PROFILE")
print("=" * 70)

print(f"\nRows    : {len(df):,}")
print(f"Columns : {len(df.columns):,}")

print("\n--- COLUMNS ---")
for i, col in enumerate(df.columns, 1):
    print(f"{i:02d}. {col}")

print("\n--- DATA TYPES ---")
print(df.dtypes.to_string())

print("\n--- MISSING VALUES ---")
missing = (
    df.isna()
      .sum()
      .sort_values(ascending=False)
)

print(missing[missing > 0].to_string())

print("\n--- DUPLICATES ---")
print(f"Duplicate rows: {df.duplicated().sum():,}")

print("\n--- SAMPLE ---")
print(df.head(5).to_string())

print("\n--- NUMERICAL SUMMARY ---")
print(df.describe(include="all").T.to_string())