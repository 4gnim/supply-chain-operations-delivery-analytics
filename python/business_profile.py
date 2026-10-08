from pathlib import Path
import pandas as pd

RAW_FILE = Path("data/raw/DataCoSupplyChainDataset.csv")

df = pd.read_csv(RAW_FILE, encoding="latin1")

print("=" * 70)
print("BUSINESS PROFILING")
print("=" * 70)

# -----------------------------
# 1. Key uniqueness
# -----------------------------
print("\n--- KEY UNIQUENESS ---")
for col in ["Order Id", "Order Item Id", "Customer Id", "Product Card Id"]:
    print(f"{col}:")
    print(f"  unique values : {df[col].nunique():,}")
    print(f"  duplicates    : {df[col].duplicated().sum():,}")

# -----------------------------
# 2. Date range
# -----------------------------
print("\n--- DATE RANGE ---")

df["order_date"] = pd.to_datetime(
    df["order date (DateOrders)"],
    errors="coerce"
)

df["shipping_date"] = pd.to_datetime(
    df["shipping date (DateOrders)"],
    errors="coerce"
)

print("Order date:")
print("  min:", df["order_date"].min())
print("  max:", df["order_date"].max())

print("Shipping date:")
print("  min:", df["shipping_date"].min())
print("  max:", df["shipping_date"].max())

# -----------------------------
# 3. Business dimensions
# -----------------------------
dimensions = [
    "Delivery Status",
    "Shipping Mode",
    "Order Status",
    "Market",
    "Customer Segment",
    "Order Region",
    "Department Name",
]

for col in dimensions:
    print(f"\n--- {col.upper()} ---")
    print(df[col].value_counts(dropna=False).to_string())

# -----------------------------
# 4. Category
# -----------------------------
print("\n--- TOP 20 CATEGORIES ---")
print(
    df["Category Name"]
    .value_counts()
    .head(20)
    .to_string()
)

# -----------------------------
# 5. Financial totals
# -----------------------------
print("\n--- FINANCIAL SUMMARY ---")

print(f"Sales total        : {df['Sales'].sum():,.2f}")
print(f"Order Item Total   : {df['Order Item Total'].sum():,.2f}")
print(f"Profit total       : {df['Order Profit Per Order'].sum():,.2f}")
print(f"Quantity total     : {df['Order Item Quantity'].sum():,.0f}")
print(f"Discount total     : {df['Order Item Discount'].sum():,.2f}")

# -----------------------------
# 6. Shipping performance
# -----------------------------
print("\n--- SHIPPING PERFORMANCE ---")

print(
    "Avg actual shipping days   :",
    round(df["Days for shipping (real)"].mean(), 2)
)

print(
    "Avg scheduled shipping days:",
    round(df["Days for shipment (scheduled)"].mean(), 2)
)

print(
    "Avg shipping delay:",
    round(
        (
            df["Days for shipping (real)"]
            - df["Days for shipment (scheduled)"]
        ).mean(),
        2
    )
)

# -----------------------------
# 7. Delivery status vs risk
# -----------------------------
print("\n--- DELIVERY STATUS vs LATE RISK ---")

print(
    pd.crosstab(
        df["Delivery Status"],
        df["Late_delivery_risk"],
        margins=True
    )
)

print("\n--- ORDER-LEVEL CONSISTENCY ---")

check_cols = [
    "Delivery Status",
    "Shipping Mode",
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Late_delivery_risk",
]

for col in check_cols:
    counts = df.groupby("Order Id")[col].nunique(dropna=False)
    inconsistent = (counts > 1).sum()

    print(f"{col}:")
    print(f"  Orders with multiple values: {inconsistent:,}")


print("\n--- ORDER-LEVEL DELIVERY METRICS ---")

order_df = (
    df.groupby("Order Id", as_index=False)
      .agg(
          delivery_status=("Delivery Status", "first"),
          shipping_mode=("Shipping Mode", "first"),
          actual_shipping_days=("Days for shipping (real)", "first"),
          scheduled_shipping_days=("Days for shipment (scheduled)", "first"),
          late_risk=("Late_delivery_risk", "first"),
          sales=("Sales", "sum"),
          profit=("Order Profit Per Order", "sum"),
          quantity=("Order Item Quantity", "sum"),
      )
)

print(f"Orders: {len(order_df):,}")

print("\nDelivery status:")
print(order_df["delivery_status"].value_counts())

print("\nShipping mode:")
print(order_df["shipping_mode"].value_counts())

print("\nOrder-level late delivery rate:")
print(
    (order_df["delivery_status"] == "Late delivery").mean() * 100
)

print("\nAverage actual shipping days:")
print(order_df["actual_shipping_days"].mean())

print("\nAverage scheduled shipping days:")
print(order_df["scheduled_shipping_days"].mean())


print("\n--- ORDER PROFIT CONSISTENCY ---")

profit_check = (
    df.groupby("Order Id")["Order Profit Per Order"]
      .nunique(dropna=False)
)

print(
    "Orders with multiple profit values:",
    (profit_check > 1).sum()
)

print(
    "Orders with single profit value:",
    (profit_check == 1).sum()
)

print("\n--- SAMPLE ORDER PROFIT ---")

sample_order = df["Order Id"].iloc[0]

print(
    df.loc[
        df["Order Id"] == sample_order,
        [
            "Order Id",
            "Order Item Id",
            "Sales",
            "Order Item Total",
            "Order Item Profit Ratio",
            "Order Profit Per Order"
        ]
    ].to_string(index=False)
)


print("\n--- PROFIT FORMULA VALIDATION ---")

df["calculated_profit"] = (
    df["Order Item Total"] * df["Order Item Profit Ratio"]
)

df["profit_diff"] = (
    df["Order Profit Per Order"] - df["calculated_profit"]
).abs()

print(
    "Max absolute difference:",
    df["profit_diff"].max()
)

print(
    "Rows with difference > 0.01:",
    (df["profit_diff"] > 0.01).sum()
)

print(
    "Rows with difference > 0.0001:",
    (df["profit_diff"] > 0.0001).sum()
)

print("\nSample validation:")
print(
    df[
        [
            "Order Item Total",
            "Order Item Profit Ratio",
            "Order Profit Per Order",
            "calculated_profit",
            "profit_diff"
        ]
    ].head(10).to_string(index=False)
)


print("\n--- BENEFIT vs ORDER PROFIT ---")

benefit_diff = (
    df["Benefit per order"] - df["Order Profit Per Order"]
).abs()

print(
    "Max absolute difference:",
    benefit_diff.max()
)

print(
    "Rows with difference > 0.0001:",
    (benefit_diff > 0.0001).sum()
)

print("\nSample:")
print(
    df[
        [
            "Benefit per order",
            "Order Profit Per Order"
        ]
    ].head(10).to_string(index=False)
)