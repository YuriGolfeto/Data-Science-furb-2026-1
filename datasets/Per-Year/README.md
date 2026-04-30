# Per-Year Datasets — Documentation

## What is in this folder?

This folder contains yearly summary files for the year **2025**, derived from the cleaned quarterly datasets.

There are **two Excel files**, one for each indicator:

| File | Description |
|---|---|
| `gdp_2025.xlsx` | Average GDP per capita for each country in 2025 |
| `unemployment_2025.xlsx` | Average unemployment rate for each country in 2025 |

---

## How the data was processed

### Step 1 — Load the cleaned quarterly data

The source files are the cleaned datasets produced in Unit 2:
- `datasets/gdp_per_capita_cleaned.csv` — GDP per capita, one row per country per quarter
- `datasets/unemployment_quarterly_cleaned.csv` — Unemployment rate, one row per country per quarter

### Step 2 — Filter to 2025 only

Only rows where the quarter starts with `2025` were kept (Q1, Q2, Q3, Q4 of 2025).
The original data also contains `2024Q4` (GDP) and `2026Q1` (Unemployment), which were excluded.

### Step 3 — Average across quarters (one row per country)

For each country, the four quarterly values were averaged into a single number representing the year.

- **GDP:** arithmetic mean of `GDP_PER_CAPITA_USD_PPP` across available 2025 quarters → stored as `GDP_PER_CAPITA_USD_PPP_AVG_2025`
- **Unemployment:** arithmetic mean of `UNE_RATE_PCT` across available 2025 quarters → stored as `UNE_RATE_PCT_AVG_2025`

Using the mean is appropriate here because both indicators are ratio-scale values (USD per person and percentage), so averaging quarters gives a meaningful yearly estimate.

### Step 4 — Export to Excel

The resulting table (one row per country, sorted alphabetically by country code) was exported to `.xlsx`.

A column `QUARTERS_USED` is included to show how many quarters were available for each country's average (normally 4, but some countries may have fewer due to missing data).

---

## Columns in each file

### gdp_2025.xlsx

| Column | Description |
|---|---|
| `REF_AREA` | ISO 3-letter country code (e.g. `USA`, `DEU`) |
| `GDP_PER_CAPITA_USD_PPP_AVG_2025` | Average GDP per capita in 2025, in constant 2020 USD (PPP-adjusted) |
| `QUARTERS_USED` | Number of quarters included in the average (max 4) |

### unemployment_2025.xlsx

| Column | Description |
|---|---|
| `REF_AREA` | ISO 3-letter country code |
| `UNE_RATE_PCT_AVG_2025` | Average unemployment rate in 2025, as % of labour force (age 15+) |
| `QUARTERS_USED` | Number of quarters included in the average (max 4) |

---

## Notes

- **Ireland (IRL)** has an unusually high GDP per capita (~$126,000 USD PPP) due to multinational corporations booking profits through Irish subsidiaries. This is a known structural distortion and does not reflect the actual living standard of Irish residents.
- **Luxembourg (LUX)** also has an elevated GDP per capita due to a large cross-border workforce that contributes to output but is not counted as residents.
- These two countries are treated as structural outliers in the hypothesis testing phase of this project.
