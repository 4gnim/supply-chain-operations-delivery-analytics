from pathlib import Path
import pandas as pd

RAW_FILE = Path("data/raw/DataCoSupplyChainDataset.csv")
OUTPUT_FILE = Path("data/processed/supply_chain_clean.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW_FILE, encoding="latin1")

# --------------------------------------------------
# Rename / parse dates
# --------------------------------------------------
df["order_date"] = pd.to_datetime(
    df["order date (DateOrders)"],
    errors="coerce"
)

df["shipping_date"] = pd.to_datetime(
    df["shipping date (DateOrders)"],
    errors="coerce"
)

# --------------------------------------------------
# Derived fields
# --------------------------------------------------
df["shipping_delay_days"] = (
    df["Days for shipping (real)"]
    - df["Days for shipment (scheduled)"]
)

df["order_year"] = df["order_date"].dt.year
df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

# Recorded profit/benefit at order-item level
df["profit"] = df["Benefit per order"]

# --------------------------------------------------
# Keep only relevant analytical columns
# --------------------------------------------------
columns = [
    "Order Id",
    "Order Item Id",
    "Customer Id",
    "Product Card Id",

    "order_date",
    "shipping_date",
    "order_year",
    "order_month",

    "Delivery Status",
    "Late_delivery_risk",
    "Shipping Mode",
    "Order Status",

    "Customer Segment",
    "Market",
    "Order Region",
    "Order Country",
    "Order State",
    "Order City",

    "Department Name",
    "Category Name",
    "Product Name",

    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "shipping_delay_days",

    "Order Item Quantity",
    "Sales",
    "Order Item Total",
    "Order Item Discount",
    "Order Item Discount Rate",
    "profit",
    "Order Item Profit Ratio",
]

clean_df = df[columns].copy()

# --------------------------------------------------
# Validation
# --------------------------------------------------
assert clean_df["Order Item Id"].duplicated().sum() == 0
assert clean_df["Order Id"].notna().all()
assert clean_df["order_date"].notna().all()
assert clean_df["shipping_date"].notna().all()

# --------------------------------------------------
# Save
# --------------------------------------------------
clean_df.to_csv(OUTPUT_FILE, index=False)

print("=" * 70)
print("CLEAN DATASET CREATED")
print("=" * 70)

print(f"Rows    : {len(clean_df):,}")
print(f"Columns : {len(clean_df.columns):,}")
print(f"Output  : {OUTPUT_FILE}")

print("\nMissing values:")
print(
    clean_df.isna()
    .sum()
    .loc[lambda x: x > 0]
    .sort_values(ascending=False)
)

print("\nDate range:")
print(clean_df["order_date"].min(), "to", clean_df["order_date"].max())

print("\nShipping delay:")
print(clean_df["shipping_delay_days"].describe())