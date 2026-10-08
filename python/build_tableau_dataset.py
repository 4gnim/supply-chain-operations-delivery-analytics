from pathlib import Path
import pandas as pd

INPUT_FILE = Path("data/processed/supply_chain_clean.csv")
OUTPUT_FILE = Path("data/processed/tableau_master.csv")

df = pd.read_csv(INPUT_FILE)

# --------------------------------------------------
# ORDER-LEVEL FLAG
# --------------------------------------------------

# Sort order items so the first record of every order
# can be identified consistently.
df = df.sort_values(
    ["Order Id", "Order Item Id"]
).reset_index(drop=True)

df["order_item_number"] = (
    df.groupby("Order Id").cumcount() + 1
)

df["is_first_order_item"] = (
    df["order_item_number"] == 1
).astype(int)

# --------------------------------------------------
# ORDER-LEVEL SHIPPING FIELDS
# Only populate them once per order.
# --------------------------------------------------

df["order_actual_shipping_days"] = df["Days for shipping (real)"].where(
    df["is_first_order_item"] == 1
)

df["order_scheduled_shipping_days"] = df[
    "Days for shipment (scheduled)"
].where(
    df["is_first_order_item"] == 1
)

df["order_shipping_delay_days"] = df[
    "shipping_delay_days"
].where(
    df["is_first_order_item"] == 1
)

# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

total_orders = df["Order Id"].nunique()

first_item_count = df["is_first_order_item"].sum()

assert total_orders == first_item_count, (
    f"Order mismatch: {total_orders} orders "
    f"but {first_item_count} first-order records."
)

assert df["Order Item Id"].duplicated().sum() == 0

# --------------------------------------------------
# SAVE
# --------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("=" * 70)
print("TABLEAU DATASET CREATED")
print("=" * 70)

print(f"Rows          : {len(df):,}")
print(f"Columns       : {len(df.columns):,}")
print(f"Orders        : {total_orders:,}")
print(f"First records : {first_item_count:,}")
print(f"Output        : {OUTPUT_FILE}")

print("\nOrder-level shipping field non-null counts:")

for col in [
    "order_actual_shipping_days",
    "order_scheduled_shipping_days",
    "order_shipping_delay_days",
]:
    print(
        f"{col}: {df[col].notna().sum():,}"
    )