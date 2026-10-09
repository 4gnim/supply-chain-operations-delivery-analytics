# Supply Chain Operations & Delivery Analytics

An end-to-end data analytics project analyzing supply chain operations, delivery performance, sales, profitability, and product performance using Python and Tableau.

## Project Overview

This project analyzes a large transactional supply chain dataset to identify patterns in order fulfillment, delivery performance, regional operations, product performance, and profitability.

The project follows a reproducible workflow:

```text
Raw Data
   ↓
Data Profiling
   ↓
Data Cleaning & Validation
   ↓
Analytical Data Preparation
   ↓
Tableau Dashboards
   ↓
Business Insights
```

## Business Objectives

The analysis focuses on:

- Monitoring overall sales and profitability
- Measuring delivery and shipping performance
- Identifying shipping modes and regions with higher delivery risk
- Understanding product and department performance
- Providing interactive dashboards for operational and business analysis

## Dataset

Source:

[DataCo Smart Supply Chain for Big Data Analysis](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis)

The downloaded dataset package contains three files:

- `DataCoSupplyChainDataset`
- `DescriptionDataCoSupplyChain`
- `tokenized_access_logs`

The main analysis in this project uses `DataCoSupplyChainDataset`. The description file is used as a reference for understanding variables. The `tokenized_access_logs` file is not used in the current dashboard analysis because it is outside the scope of the supply chain operations and delivery questions addressed in this project.

The main dataset contains:

- 180,519 order-item records
- 65,752 unique orders
- 20,652 unique customers
- 118 products
- 50 product categories
- 11 departments
- 5 markets
- 23 order regions

The order data covers **January 2015 through January 2018**.

## Data Grain

The source dataset is stored at the **order-item level**.

One order can contain multiple order items. Therefore:

- Orders are counted using distinct `Order Id`
- Order-item metrics are aggregated from item-level records
- Shipping metrics are evaluated at order level
- Sales and recorded profit are aggregated from the relevant transactional records

This distinction is important to prevent order counts and shipping metrics from being inflated by multi-item orders.

## Data Preparation

Python was used for the data preparation workflow, including:

- Dataset profiling
- Data type inspection
- Missing-value analysis
- Duplicate validation
- Date parsing
- Shipping-delay calculation
- Order-level consistency validation
- Removal of irrelevant fields
- Analytical dataset construction
- Creation of Tableau-ready order-level fields

The original dataset contains fields such as customer email, password, and other personal-information-related attributes that are not relevant to the dashboard analysis. These fields were excluded from the cleaned analytical dataset.

The final cleaned analytical dataset contains **180,519 rows and 31 analytical columns**.

### Validation

The following order-level attributes were checked for consistency across all order items belonging to the same order:

- Delivery Status
- Shipping Mode
- Days for shipping (real)
- Days for shipment (scheduled)
- Late delivery risk

No duplicate `Order Item Id` values were found.

## Key Metrics

| Metric                          |          Value |
| ------------------------------- | -------------: |
| Total Orders                    |         65,752 |
| Total Order Items               |        180,519 |
| Total Sales                     | $36,784,735.01 |
| Total Profit                    |  $3,966,902.97 |
| Profit Margin                   |         10.78% |
| Late Orders                     |         36,048 |
| Shipped Orders                  |         62,897 |
| Late Delivery Rate              |         57.31% |
| Average Actual Shipping Days    |           3.50 |
| Average Scheduled Shipping Days |           2.93 |
| Average Shipping Delay          |      0.57 days |
| Total Quantity                  |        384,079 |
| Total Products                  |            118 |

### KPI Definitions

**Total Orders**

Distinct count of `Order Id`.

```text
COUNTD(Order Id)
```

**Total Sales**

```text
SUM(Sales)
```

**Total Profit**

The project uses the dataset's recorded `Benefit per order` field as the profit metric. `Benefit per order` was validated against `Order Profit Per Order` and the two fields were identical across the dataset.

```text
SUM(Benefit per order)
```

**Profit Margin**

```text
Total Profit / Total Sales
```

**Shipped Orders**

Orders whose delivery status is not `Shipping canceled`.

**Late Delivery Rate**

```text
Late Orders / Shipped Orders
```

Shipping-canceled orders are excluded from the denominator.

**Shipping Delay**

```text
Actual Shipping Days - Scheduled Shipping Days
```

A negative value indicates shipment earlier than the scheduled duration, zero indicates the scheduled duration was met, and a positive value indicates additional shipping time.

## Tableau Dashboards

The Tableau workbook contains three dashboards.

### 1. Executive Overview

Provides a high-level view of business and delivery performance, including:

- Total orders
- Total sales
- Total profit
- Profit margin
- Late delivery rate
- Monthly sales trend
- Sales by market
- Delivery status

### 2. Delivery & Operations

Focuses on operational shipping performance, including:

- Late delivery rate by shipping mode
- Actual vs scheduled shipping days
- Regional delivery performance
- Shipping delay distribution
- Delivery and shipping performance by market and shipping mode

### 3. Product & Profitability

Analyzes product and department performance, including:

- Sales by department
- Top products by sales
- Bottom products by profit
- Profitability and margin indicators
- Product-level and department-level performance

The dashboards include interactive filters for relevant dimensions such as year, market, shipping mode, and department.

## Tools & Technologies

- Python
- Pandas
- Tableau
- Git
- GitHub

## Project Structure

```text
supply-chain-operations-delivery-analytics/
├── data/
│   ├── raw/
│   │   ├── DataCoSupplyChainDataset.csv
│   │   ├── DescriptionDataCoSupplyChain.csv
│   │   └── tokenized_access_logs.csv
│   └── processed/
│       ├── supply_chain_clean.csv
│       ├── tableau_master.csv
│       └── marts/
│           ├── order_performance.csv
│           ├── monthly_performance.csv
│           ├── shipping_mode_performance.csv
│           ├── region_performance.csv
│           └── category_performance.csv
├── python/
│   ├── profile_dataset.py
│   ├── business_profile.py
│   ├── clean_dataset.py
│   ├── build_marts.py
│   └── build_tableau_dataset.py
├── tableau/
│   └── supply_chain_operations_delivery.twbx
├── screenshots/
├── docs/
│   └── README.md
├── README.md
└── .gitignore
```

## Tableau Public

[View Interactive Dashboard](https://public.tableau.com/app/profile/agni.musadad/viz/SupplyChainOperationsDeliveryAnalytics/02-DeliveryOperations)

## Case Study

[Read the Full Case Study](YOUR_CASE_STUDY_LINK)

## Disclaimer

The dataset is a public dataset intended for analytical and educational use. Financial and operational metrics in this project should be interpreted within the context of the provided dataset and should not be treated as real-world company accounting or operational records.
