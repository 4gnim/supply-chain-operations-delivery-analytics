# Data

This directory contains the source and processed datasets used in the project.

## Dataset Source

The project uses the public **DataCo Smart Supply Chain for Big Data Analysis** dataset.

Source:
https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis

The dataset package contains three main files:

- `DataCoSupplyChainDataset`
- `DescriptionDataCoSupplyChain`
- `tokenized_access_logs`

## Dataset Usage

### DataCoSupplyChainDataset

The primary transactional dataset used for supply chain, delivery, sales, and profitability analysis.

The dataset contains:

- 180,519 order-item records
- 65,752 unique orders
- 20,652 customers
- 118 products
- 50 categories
- 11 departments
- 5 markets
- 23 order regions

### DescriptionDataCoSupplyChain

The variable description/reference file used to understand the meaning and context of the fields in the main dataset.

### tokenized_access_logs

This file contains access/clickstream-related information. It was not used in the main analytical workflow because the project focuses on supply chain operations, delivery performance, sales, profitability, and product analysis.

## Data Processing

The raw dataset was processed using Python through the scripts in the `python/` directory.

The workflow includes:

1. Dataset profiling
2. Missing-value inspection
3. Duplicate validation
4. Date parsing
5. Data cleaning
6. Order-level consistency validation
7. Shipping-delay calculation
8. Analytical mart construction
9. Tableau dataset preparation

## Analytical Dataset

The final Tableau-ready dataset is generated as:

```text
data/processed/tableau_master.csv
```

Supporting analytical marts are generated under:

```text
data/processed/marts/
```

These generated CSV files are excluded from Git version control because of their size.

## Reproducing the Data Preparation

Run the scripts from the project root in the following order:

```bash
python python/profile_dataset.py
python python/business_profile.py
python python/clean_dataset.py
python python/build_marts.py
python python/build_tableau_dataset.py
```

The scripts expect the source dataset to be placed under:

```text
data/raw/
```

## Privacy Considerations

The raw dataset contains fields such as customer names, addresses, email placeholders, and password placeholders.

These fields were excluded from the final analytical dataset when they were not relevant to the business questions.

The project does not publish raw customer-level data to the GitHub repository.
