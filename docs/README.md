# Supply Chain Operations & Delivery Analytics — Case Study

## 1. Business Context

Supply chain performance affects customer experience, operational efficiency, and overall business performance.

This project examines a transactional supply chain dataset to understand how orders perform across delivery, shipping modes, regions, departments, and products.

The analysis focuses on identifying operational patterns that can support better monitoring and data-driven decision-making.

## 2. Business Questions

### Business Performance

- How are sales and profitability distributed across the business?
- How does sales performance change over time?
- Which markets contribute the most sales?
- Which departments contribute the most sales and profit?

### Delivery Performance

- What proportion of shipped orders experience late delivery?
- Which shipping modes have higher late-delivery rates?
- How does actual shipping time compare with scheduled shipping time?
- Which regions show higher delivery risk?
- How is shipping delay distributed?

### Product Performance

- Which products generate the highest sales?
- Which products have the weakest recorded profitability?
- How does product performance differ across departments?

## 3. Dataset

The project uses the **DataCo Smart Supply Chain for Big Data Analysis** dataset from Kaggle.

Dataset source:

https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis

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

## 4. Data Preparation

The raw dataset was profiled and prepared using Python.

The workflow included:

1. Dataset profiling
2. Data type inspection
3. Missing-value analysis
4. Duplicate validation
5. Date conversion
6. Shipping-delay calculation
7. Order-level consistency checks
8. Removal of irrelevant fields
9. Creation of cleaned analytical data
10. Creation of Tableau-ready fields and analytical marts

### Data Quality Findings

The source dataset contained fields that were not relevant to the analytical objective, including customer email/password placeholders and other personal-information-related attributes. These were excluded from the final analytical dataset.

`Product Description` was entirely missing in the downloaded main dataset and was excluded from the analytical dataset.

`Order Zipcode` contained a large proportion of missing values and was also excluded because it was not required for the dashboard questions.

There were no duplicate `Order Item Id` values.

### Order-Level Consistency

The following fields were checked within each `Order Id`:

- Delivery Status
- Shipping Mode
- Days for shipping (real)
- Days for shipment (scheduled)
- Late delivery risk

All five fields were consistent within each order in the downloaded dataset.

## 5. Data Grain

The source dataset is at the **order-item level**.

This means one order can contain multiple items. Therefore, the project distinguishes between order-level and order-item-level analysis.

Examples:

- Total Orders uses a distinct count of `Order Id`
- Order-item quantities are summed from the transactional rows
- Shipping performance uses one validated shipping record per order
- Sales and recorded profit are aggregated from the order-item records

This approach prevents multi-item orders from being counted as multiple orders.

## 6. KPI Definitions

### Total Orders

Distinct number of orders.

```text
COUNTD(Order Id)
```

### Total Sales

```text
SUM(Sales)
```

### Total Profit

The dataset contains both `Benefit per order` and `Order Profit Per Order`. These two fields were validated and found to be identical across all records. The project therefore uses `Benefit per order` as the recorded profit metric.

```text
SUM(Benefit per order)
```

### Profit Margin

```text
Total Profit / Total Sales
```

### Shipped Orders

Orders with a delivery status other than `Shipping canceled`.

### Late Delivery Rate

```text
Late Orders / Shipped Orders
```

Shipping-canceled orders are excluded from the denominator.

### Shipping Delay

```text
Actual Shipping Days - Scheduled Shipping Days
```

Negative values represent faster-than-scheduled shipment, zero represents the scheduled duration, and positive values represent additional shipping time.

## 7. Key Results

### Overall Business Performance

The dataset contains **65,752 orders** and **180,519 order-item records**.

Recorded sales total **$36,784,735.01**, while recorded profit totals **$3,966,902.97**, resulting in a **10.78% profit margin** based on the dataset's recorded profit field.

### Delivery Performance

Delivery performance is a major operational focus of the project.

There are **36,048 late orders** among **62,897 shipped orders**, resulting in a **57.31% late-delivery rate**.

Average actual shipping time is **3.50 days**, compared with an average scheduled shipping time of **2.93 days**, producing an average shipping delay of approximately **0.57 days**.

### Product and Department Performance

Sales and profitability are not distributed evenly across departments and products. The product dashboard is designed to identify high-sales products and products with comparatively weak recorded profitability for further review.

### Important Interpretation Note

The financial values come directly from the public dataset and are used for analytical practice. They should not be interpreted as audited accounting figures or actual operational results from a real company.

## 8. Dashboard Design

### Executive Overview

Provides management-level KPIs and a high-level view of sales, profitability, market performance, and delivery status.

### Delivery & Operations

Provides an operational view of shipping performance, including late delivery rates, shipping duration, regional delivery risk, and shipping delay distribution.

### Product & Profitability

Provides a product and department view covering sales, profit, margin, quantity, and product performance.

Interactive filters allow users to explore the dashboards by relevant dimensions such as year, market, shipping mode, and department.

## 9. Analytical Workflow

```text
Raw Data
    ↓
Profiling
    ↓
Cleaning & Validation
    ↓
Order-Level Consistency Checks
    ↓
Analytical Data Preparation
    ↓
KPI Development
    ↓
Tableau Dashboard Development
    ↓
Interactive Analysis
```

## 10. Tools

- Python
- Pandas
- Tableau
- Git
- GitHub

## 11. Project Outputs

- Clean analytical dataset
- Tableau-ready dataset
- Analytical marts
- Interactive Tableau dashboards
- Reproducible Python preprocessing scripts
- Portfolio case study

## 12. Links

### Tableau Public

YOUR_TABLEAU_PUBLIC_LINK

### GitHub Repository

YOUR_GITHUB_REPOSITORY_LINK

### Portfolio Case Study

YOUR_CASE_STUDY_LINK
