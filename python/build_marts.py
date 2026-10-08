from pathlib import Path
import pandas as pd

INPUT_FILE = Path("data/processed/supply_chain_clean.csv")
OUTPUT_DIR = Path("data/processed/marts")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

# --------------------------------------------------
# 1. ORDER-LEVEL MART
# --------------------------------------------------

order_df = (
    df.groupby("Order Id", as_index=False)
    .agg(
        customer_id=("Customer Id", "first"),
        order_date=("order_date", "first"),
        shipping_date=("shipping_date", "first"),

        delivery_status=("Delivery Status", "first"),
        shipping_mode=("Shipping Mode", "first"),
        order_status=("Order Status", "first"),
        late_delivery_risk=("Late_delivery_risk", "first"),

        customer_segment=("Customer Segment", "first"),
        market=("Market", "first"),
        order_region=("Order Region", "first"),
        order_country=("Order Country", "first"),

        actual_shipping_days=("Days for shipping (real)", "first"),
        scheduled_shipping_days=("Days for shipment (scheduled)", "first"),
        shipping_delay_days=("shipping_delay_days", "first"),

        order_items=("Order Item Id", "count"),
        quantity=("Order Item Quantity", "sum"),
        sales=("Sales", "sum"),
        discount=("Order Item Discount", "sum"),
        profit=("profit", "sum"),
    )
)

order_df["profit_margin"] = (
    order_df["profit"] / order_df["sales"]
)

order_df["shipped_order"] = (
    order_df["delivery_status"] != "Shipping canceled"
).astype(int)

order_df["late_delivery"] = (
    order_df["delivery_status"] == "Late delivery"
).astype(int)

order_df["on_time_delivery"] = (
    order_df["delivery_status"] == "Shipping on time"
).astype(int)

order_df["advance_shipping"] = (
    order_df["delivery_status"] == "Advance shipping"
).astype(int)

order_df["canceled_shipping"] = (
    order_df["delivery_status"] == "Shipping canceled"
).astype(int)

order_df.to_csv(
    OUTPUT_DIR / "order_performance.csv",
    index=False
)

# --------------------------------------------------
# 2. MONTHLY PERFORMANCE
# --------------------------------------------------

df["month"] = pd.to_datetime(df["order_date"]).dt.to_period("M").astype(str)

monthly = (
    df.groupby("month", as_index=False)
    .agg(
        sales=("Sales", "sum"),
        profit=("profit", "sum"),
        quantity=("Order Item Quantity", "sum"),
        order_items=("Order Item Id", "count"),
        orders=("Order Id", "nunique"),
    )
)

monthly["profit_margin"] = (
    monthly["profit"] / monthly["sales"]
)

monthly.to_csv(
    OUTPUT_DIR / "monthly_performance.csv",
    index=False
)

# --------------------------------------------------
# 3. SHIPPING MODE PERFORMANCE
# --------------------------------------------------

shipping_mode = (
    order_df.groupby("shipping_mode", as_index=False)
    .agg(
        orders=("Order Id", "count"),
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        avg_actual_shipping_days=("actual_shipping_days", "mean"),
        avg_scheduled_shipping_days=("scheduled_shipping_days", "mean"),
        avg_shipping_delay=("shipping_delay_days", "mean"),
        late_orders=("late_delivery", "sum"),
        on_time_orders=("on_time_delivery", "sum"),
        advance_orders=("advance_shipping", "sum"),
        canceled_orders=("canceled_shipping", "sum"),
    )
)

shipping_mode["shipped_orders"] = (
    shipping_mode["late_orders"]
    + shipping_mode["on_time_orders"]
    + shipping_mode["advance_orders"]
)

shipping_mode["late_delivery_rate"] = (
    shipping_mode["late_orders"]
    / shipping_mode["shipped_orders"]
)

shipping_mode["profit_margin"] = (
    shipping_mode["profit"]
    / shipping_mode["sales"]
)

shipping_mode.to_csv(
    OUTPUT_DIR / "shipping_mode_performance.csv",
    index=False
)

# --------------------------------------------------
# 4. REGION PERFORMANCE
# --------------------------------------------------

region = (
    order_df.groupby("order_region", as_index=False)
    .agg(
        orders=("Order Id", "count"),
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        quantity=("quantity", "sum"),
        avg_shipping_delay=("shipping_delay_days", "mean"),
        late_orders=("late_delivery", "sum"),
        shipped_orders=("shipped_order", "sum"),
        canceled_orders=("canceled_shipping", "sum"),
    )
)

region["late_delivery_rate"] = (
    region["late_orders"]
    / region["shipped_orders"]
)

region["profit_margin"] = (
    region["profit"]
    / region["sales"]
)

region.to_csv(
    OUTPUT_DIR / "region_performance.csv",
    index=False
)

# --------------------------------------------------
# 5. CATEGORY PERFORMANCE
# --------------------------------------------------

category = (
    df.groupby("Category Name", as_index=False)
    .agg(
        order_items=("Order Item Id", "count"),
        orders=("Order Id", "nunique"),
        quantity=("Order Item Quantity", "sum"),
        sales=("Sales", "sum"),
        profit=("profit", "sum"),
        discount=("Order Item Discount", "sum"),
    )
)

category["profit_margin"] = (
    category["profit"] / category["sales"]
)

category.to_csv(
    OUTPUT_DIR / "category_performance.csv",
    index=False
)

# --------------------------------------------------
# 6. SUMMARY
# --------------------------------------------------

total_orders = order_df["Order Id"].nunique()

late_orders = order_df["late_delivery"].sum()
shipped_orders = order_df["shipped_order"].sum()

late_rate = late_orders / shipped_orders

print("=" * 70)
print("ANALYTICAL MARTS CREATED")
print("=" * 70)

print(f"Orders               : {total_orders:,}")
print(f"Order items          : {len(df):,}")
print(f"Sales                : {df['Sales'].sum():,.2f}")
print(f"Profit               : {df['profit'].sum():,.2f}")
print(f"Profit margin        : {df['profit'].sum() / df['Sales'].sum():.2%}")
print(f"Late orders          : {late_orders:,}")
print(f"Shipped orders       : {shipped_orders:,}")
print(f"Late delivery rate   : {late_rate:.2%}")

print("\nOutput files:")
for file in OUTPUT_DIR.glob("*.csv"):
    print(f"- {file.name}")