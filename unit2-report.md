# Unit 2 – Practical Assignment: Data Cleaning and Preparation

**Course:** Data Science (Optativa I)  
**Professor:** Maiko Spiess  
**Date:** April 2026

---

## 1. Dataset Motivation and Contextualization

### Domain and Context

This assignment explores the relationship between **economic output** and **labor market conditions** across OECD member countries and selected partner economies. The analysis draws on two official datasets published by the Organisation for Economic Co-operation and Development (OECD):

1. **DF_QNA_EXPENDITURE_CAPITA** — *Quarterly GDP per Capita (Expenditure Approach)*  
   Gross Domestic Product per capita measured in US dollars per person, PPP-converted, calendar and seasonally adjusted. GDP is computed via the expenditure approach: household consumption + government consumption + gross fixed capital formation + net trade (exports − imports). Data covers OECD members, G7, G20, the European Union, the euro area, and selected other economies.

2. **DF_IALFS_UNE_M** — *Monthly Unemployment Rates*  
   Monthly unemployment rate expressed as a percentage of the labour force, for the population aged 15 and over, disaggregated by sex. Data follows the ILO definition adopted at the 19th Conference of Labour Statisticians (2013), ensuring international comparability across all OECD member countries.

### Research Motivation

The central question driving this work is:

> **To what extent does a country's economic output (GDP per capita) relate to the employment conditions of its population over time?**

This question is grounded in macroeconomic theory: higher economic output per capita is generally expected to correlate with stronger labor demand and lower unemployment rates. However, the relationship is non-trivial — structural factors such as labor market regulation, industry composition, social protection systems, and technological change can decouple GDP growth from employment gains (a phenomenon sometimes referred to as *jobless growth*). Cross-country comparison across OECD economies provides a natural experimental setting to observe how different institutional contexts mediate this relationship.

### Relevance

- **Economic relevance:** GDP per capita and unemployment are two of the most closely monitored macroeconomic indicators by governments, central banks, and international institutions. Understanding their joint dynamics informs fiscal and monetary policy decisions.
- **Social relevance:** Unemployment directly impacts standards of living, mental health, social cohesion, and inequality. Comparing trends across countries helps identify lagging economies and potential policy lessons.
- **Scientific relevance:** The dataset spans multiple countries and decades, enabling time-series and panel data analyses. It allows testing of classical hypotheses such as Okun's Law, which posits an empirical inverse relationship between GDP growth and unemployment.
- **Technical relevance:** Both datasets require non-trivial preprocessing — resolving different temporal granularities (quarterly vs. monthly), aligning country codes, handling missing observations, and merging on common keys — making them an ideal case study for data wrangling.

### Potential Analytical Use Cases

- **Descriptive analysis:** Characterize the distribution of unemployment and GDP per capita across countries and time periods; identify outliers (e.g., countries with high GDP but also high unemployment, or vice versa).
- **Correlation and regression analysis:** Quantify the strength of the relationship between GDP per capita and unemployment rate across OECD countries.
- **Time-series analysis:** Examine how shocks (e.g., the 2008 financial crisis, the COVID-19 pandemic) affected both indicators simultaneously across different economies.
- **Clustering / classification:** Group countries by similar economic-employment profiles and investigate what structural characteristics distinguish these clusters.
- **Forecasting:** Use historical GDP per capita trends to predict future unemployment dynamics (or vice versa).

### Dataset Characteristics

| Attribute | DF_QNA_EXPENDITURE_CAPITA | DF_IALFS_UNE_M |
|---|---|---|
| **Type** | Structured (tabular, CSV) | Structured (tabular, CSV) |
| **Granularity** | Quarterly | Monthly |
| **Unit of measure** | USD per person (PPP-converted) | % of labour force |
| **Coverage** | OECD + G7, G20, EU, euro area | OECD member countries |
| **Data points (unfiltered, OECD total)** | ~15,095 | ~446,712 |
| **Rows in downloaded file** | 452 | 515 |
| **Last updated** | April 1, 2026 | March 31, 2026 |
| **Key identifier columns** | `REF_AREA`, `TIME_PERIOD` | `REF_AREA`, `TIME_PERIOD` |
| **Source** | OECD National Accounts (QNA) | OECD Labour Force Statistics (IALFS) |

Both datasets are **structured**, tabular, and share a common key (`REF_AREA` for country code and `TIME_PERIOD` for the observation date), which enables merging after temporal alignment (quarterly aggregation of monthly unemployment data). The files used in this assignment are filtered exports from the OECD Data Explorer, covering the most recent available periods. The GDP file (452 rows) contains **two entries per country-period** — one for current prices (`PRICE_BASE=V`) and one for constant prices (`PRICE_BASE=LR`) — which is a structural characteristic of the SDMX export format. The unemployment file (515 rows) is monthly and covers a 13-month window (February 2025 – February 2026).

---

## 2. Data Dictionary

Both datasets follow the OECD SDMX-CSV format, which interleaves coded columns with empty separator columns (labelled `Unnamed: N` by pandas). All `Unnamed` columns are entirely null and carry no analytical value — they are artefacts of the export format and will be dropped during cleaning.

### 2.1 DF_QNA_EXPENDITURE_CAPITA — GDP per Capita (Quarterly)

**Shape (raw):** 452 rows × 48 columns

| Column | Description | Data Type | Unit / Values | Quality Notes |
|---|---|---|---|---|
| `STRUCTURE` | Type of SDMX structure | Categorical | Always `DATAFLOW` | Constant — drop after validation |
| `STRUCTURE_ID` | Full dataset identifier | Categorical | `OECD.SDD.NAD:DSD_NAMAIN1@DF_QNA_EXPENDITURE_CAPITA(1.1)` | Constant — drop after validation |
| `STRUCTURE_NAME` | Human-readable name | Text | Always null in this export | Entirely missing — drop |
| `ACTION` | Data action code | Categorical | Always `I` (Insert) | Constant — drop |
| `FREQ` | Observation frequency | Categorical | `Q` (Quarterly) | Constant in this dataset |
| `ADJUSTMENT` | Seasonal/calendar adjustment flag | Categorical | `Y` (calendar & seasonally adjusted) | Constant in this dataset |
| `REF_AREA` | ISO 3-letter country/area code | Categorical | e.g. `AUS`, `HUN`, `POL` | **Key join column**; 47 unique values |
| `SECTOR` | Institutional sector | Categorical | `S1` (Total economy) | Constant — drop |
| `COUNTERPART_SECTOR` | Counterpart sector | Categorical | `S1` | Constant — drop |
| `TRANSACTION` | National accounts transaction code | Categorical | `B1GQ_POP` (GDP per capita) | Constant — drop |
| `INSTR_ASSET` | Instrument/asset type | Categorical | `_Z` (not applicable) | Constant — drop |
| `ACTIVITY` | Economic activity breakdown | Categorical | `_Z` (not applicable) | Constant — drop |
| `EXPENDITURE` | Expenditure category | Categorical | `_Z` (not applicable) | Constant — drop |
| `UNIT_MEASURE` | Unit of measurement code | Categorical | `USD_PPP_PS` (USD per person, PPP) | Constant — drop after validation |
| `PRICE_BASE` | Price base code | Categorical | `V` (current prices), `LR` (fixed prices, reference year) | Two distinct methodologies in same dataset — flag for analysis |
| `TRANSFORMATION` | Data transformation applied | Categorical | `LA` (annual level) | Constant — drop |
| `TABLE_IDENTIFIER` | OECD table reference | Categorical | `T0102` | Constant — drop |
| `TIME_PERIOD` | Reference period | Datetime (string `YYYY-QN`) | `2024-Q4` to `2025-Q4` | **Key join column**; needs parsing |
| `OBS_VALUE` | GDP per capita observation | Numerical (float) | USD per person (PPP); range varies by country | **Target variable**; 0 missing values |
| `REF_YEAR_PRICE` | Reference year for fixed-price series | Numerical (float) | `2020.0` or null | 226 missing (50%) — only populated for `PRICE_BASE = LR` rows |
| `BASE_PER` | Base period for index series | Datetime | Always null in this export | Entirely missing — drop |
| `CONF_STATUS` | Confidentiality status | Categorical | `F` (free) | Constant — drop |
| `DECIMALS` | Number of decimal places | Integer | `1` | Constant — drop |
| `OBS_STATUS` | Observation status flag | Categorical | `A` (normal), `P` (provisional), `E` (estimated) | Relevant for data quality assessment |
| `UNIT_MULT` | Unit multiplier (power of 10) | Integer | `0` (no multiplier) | Constant — drop |
| `CURRENCY` | Currency code | Categorical | `USD` | Constant — drop |
| `Unnamed: N` (×24) | Empty separator columns | — | All null | SDMX export artefact — drop all |

---

### 2.2 DF_IALFS_UNE_M — Monthly Unemployment Rate

**Shape (raw):** 515 rows × 34 columns

| Column | Description | Data Type | Unit / Values | Quality Notes |
|---|---|---|---|---|
| `STRUCTURE` | Type of SDMX structure | Categorical | Always `DATAFLOW` | Constant — drop after validation |
| `STRUCTURE_ID` | Full dataset identifier | Categorical | `OECD.SDD.TPS:DSD_LFS@DF_IALFS_UNE_M(1.0)` | Constant — drop after validation |
| `STRUCTURE_NAME` | Human-readable name | Text | Always null in this export | Entirely missing — drop |
| `ACTION` | Data action code | Categorical | Always `I` (Insert) | Constant — drop |
| `REF_AREA` | ISO 3-letter country/area code | Categorical | e.g. `CAN`, `USA`, `GBR` | **Key join column**; 43 unique values |
| `MEASURE` | Measure type code | Categorical | `UNE_LF_M` (Monthly unemployment rate) | Constant — drop after validation |
| `UNIT_MEASURE` | Unit of measurement code | Categorical | `PT_LF_SUB` (% of labour force subgroup) | Constant — drop after validation |
| `TRANSFORMATION` | Data transformation applied | Categorical | `_Z` (none) | Constant — drop |
| `ADJUSTMENT` | Seasonal adjustment flag | Categorical | `Y` (seasonally adjusted) | Constant in this dataset |
| `SEX` | Sex disaggregation | Categorical | `_T` (total, both sexes) | Constant in this filtered export |
| `AGE` | Age group | Categorical | `Y_GE15` (15 years and over) | Constant in this filtered export |
| `ACTIVITY` | Activity status | Categorical | `_Z` (not applicable) | Constant — drop |
| `FREQ` | Observation frequency | Categorical | `M` (Monthly) | Constant in this dataset |
| `TIME_PERIOD` | Reference period | Datetime (string `YYYY-MM`) | `2025-02` to `2026-02` | **Key join column**; needs parsing and quarterly aggregation for merge |
| `OBS_VALUE` | Unemployment rate observation | Numerical (float) | % of labour force; range varies by country | **Target variable**; 0 missing values |
| `BASE_PER` | Base period | Datetime | Always null in this export | Entirely missing — drop |
| `OBS_STATUS` | Observation status flag | Categorical | `A` (normal), `E` (estimated) | Relevant for data quality assessment |
| `UNIT_MULT` | Unit multiplier (power of 10) | Integer | `0` (no multiplier) | Constant — drop |
| `DECIMALS` | Number of decimal places | Integer | `1` | Constant — drop |
| `Unnamed: N` (×17) | Empty separator columns | — | All null | SDMX export artefact — drop all |

---

### 2.3 Identified Data Quality Issues

| Issue | Dataset | Description |
|---|---|---|
| Empty separator columns | Both | 24 (GDP) and 17 (UNE) fully-null `Unnamed` columns — SDMX format artefact |
| Entirely null columns | Both | `STRUCTURE_NAME` and `BASE_PER` are null in all rows |
| Temporal granularity mismatch | Both | GDP is quarterly (`YYYY-QN`); unemployment is monthly (`YYYY-MM`) — requires aggregation before merge |
| Partial nulls in `REF_YEAR_PRICE` | GDP | 226/452 rows (50%) null — structurally expected (only for `PRICE_BASE = LR` rows), not random missingness |
| Mixed `PRICE_BASE` values | GDP | `V` (current prices) and `LR` (constant prices, reference year 2020) coexist — analysis must choose one |
| Country coverage asymmetry | Both | GDP covers 47 areas; UNE covers 43 — inner join will reduce scope |
| Aggregate area codes in GDP | GDP | `REF_AREA` includes non-country aggregates: `EA20`, `EU27_2020`, `G7`, `OECD`, `OECDE`, `USMCA` — these must be excluded from country-level analysis |
| High share of provisional data | GDP | 136 rows (30%) have `OBS_STATUS=P` (provisional) and 16 rows (3.5%) have `E` (estimated); only 300 rows (66%) are final (`A`) |

---

## 3. Initial Data Cleaning and Preparation

### 3.1 Duplicate Detection and Handling

**Detection strategy:** Two-level check — (1) full-row exact comparison using `pandas.DataFrame.duplicated()`; (2) partial duplicate check on the analytical key `REF_AREA` + `TIME_PERIOD`.

**Results:**

| Dataset | Exact duplicates | Key-level partial duplicates |
|---|---|---|
| GDP | 0 | **226** |
| Unemployment | 0 | 0 |

**GDP — 226 structural partial duplicates:** Each country-period combination appears exactly twice in the raw file — once with `PRICE_BASE=V` (current prices) and once with `PRICE_BASE=LR` (constant prices, reference year 2020). These are not data entry errors; they are a deliberate feature of the SDMX export format that bundles two methodological variants into a single file.

**Treatment — Filter to `PRICE_BASE=LR`:** Only the constant-price series is retained. This is the methodologically appropriate choice for cross-country and cross-time comparison, as it removes the effect of inflation and makes GDP values comparable across periods. This filter eliminates all 226 structural partial duplicates, reducing the GDP dataset from 452 to 226 rows. No further deduplication is required.

---

### 3.2 Missing Data Treatment

#### Structural / Constant Columns (Drop)

The following columns are dropped because they are either entirely null, entirely constant (no information), or SDMX format artefacts:

**GDP dataset — columns dropped:**
`STRUCTURE`, `STRUCTURE_ID`, `STRUCTURE_NAME`, `ACTION`, `SECTOR`, `COUNTERPART_SECTOR`, `TRANSACTION`, `INSTR_ASSET`, `ACTIVITY`, `EXPENDITURE`, `TRANSFORMATION`, `TABLE_IDENTIFIER`, `BASE_PER`, `CONF_STATUS`, `DECIMALS`, `UNIT_MULT`, `CURRENCY`, and all 24 `Unnamed` columns.

**Unemployment dataset — columns dropped:**
`STRUCTURE`, `STRUCTURE_ID`, `STRUCTURE_NAME`, `ACTION`, `MEASURE`, `TRANSFORMATION`, `ACTIVITY`, `BASE_PER`, `DECIMALS`, `UNIT_MULT`, and all 17 `Unnamed` columns.

#### `REF_YEAR_PRICE` — Structural Missing (MCAR-equivalent)

In the GDP dataset, `REF_YEAR_PRICE` is null for all rows where `PRICE_BASE = V` (current prices). This is **not random missingness** — it is structurally absent because a reference year only applies to constant-price series. Classification: **MCAR-equivalent** (missingness is fully explained by another observed variable and carries no bias risk).

**Treatment:** For this analysis, only the `PRICE_BASE = LR` (constant prices, reference year 2020) series will be retained, as it enables consistent cross-country and cross-time comparisons. This eliminates the missing `REF_YEAR_PRICE` values entirely.

#### `OBS_STATUS` — Data Confidence Flags

Both datasets contain `OBS_STATUS` flags indicating the confidence level of each observation. These are not missing values but quality indicators that must be accounted for in downstream analysis.

| Status | Meaning | GDP (n=452) | UNE (n=515) |
|---|---|---|---|
| `A` | Final / normal | 300 (66.4%) | 493 (95.7%) |
| `P` | Provisional | 136 (30.1%) | — |
| `E` | Estimated | 16 (3.5%) | 22 (4.3%) |

**Treatment:** Retain all observations. Provisional and estimated values are flagged and should be treated with caution in inference. No imputation is required — these are not missing, merely lower-confidence observations.

#### Aggregate Area Codes in GDP

The GDP `REF_AREA` column contains 6 non-country aggregate entries: `EA20` (Euro Area), `EU27_2020` (European Union), `G7`, `OECD` (total), `OECDE` (OECD Europe), and `USMCA`. These represent economic blocs rather than individual countries and would distort country-level comparisons.

**Treatment:** Remove these 6 × 2 = 12 rows (two per area due to PRICE_BASE split, already resolved by the LR filter) from the analytical dataset. After the `PRICE_BASE=LR` filter, 6 aggregate rows remain and are dropped, leaving **220 country-level observations** across **41 individual countries**.

#### Summary of Missing Values — Meaningful Analytical Columns

| Column | Dataset | Raw Missing | Missing % | Missingness Type | Treatment |
|---|---|---|---|---|---|
| `STRUCTURE_NAME` | Both | 452 / 515 | 100% | Structural (SDMX export) | Drop column |
| `BASE_PER` | Both | 452 / 515 | 100% | Structural (not applicable) | Drop column |
| `Unnamed: N` (×41 total) | Both | 100% each | 100% | SDMX format artefact | Drop all |
| `REF_YEAR_PRICE` | GDP | 226 / 452 | 50% | Structural — MCAR equivalent (absent only for `PRICE_BASE=V` rows) | Resolved by filtering to `LR` |
| `OBS_VALUE` | GDP | 0 / 452 | 0% | — | No action |
| `OBS_VALUE` | UNE | 0 / 515 | 0% | — | No action |
| `REF_AREA` | Both | 0 | 0% | — | No action |
| `TIME_PERIOD` | Both | 0 | 0% | — | No action |

No imputation strategies (mean, median, mode, LOCF, interpolation) were required for the analytical columns. All missingness is **structural** — fully explained by the SDMX export format and the dual price-base methodology — and is resolved through column removal and row filtering rather than value imputation.

---

## 4. Deliverables Summary

| Deliverable | Status |
|---|---|
| Short report (this document) | ✅ `unit2-report.md` |
| Data dictionary | ✅ Section 2 + `data_dictionary.csv` |
| Cleaned dataset — after duplicate removal | ✅ `datasets/gdp_per_capita_cleaned.csv` |
| Cleaned dataset — after missing data treatment | ✅ `datasets/unemployment_quarterly_cleaned.csv` |
| Merged analytical dataset | ✅ `datasets/gdp_unemployment_merged.csv` (41 countries, 4 quarters) |
| Cleaning code | ✅ `unit2-cleaning.ipynb` |

