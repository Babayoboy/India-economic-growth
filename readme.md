# India's Economic & Demographic Journey Across Prime Ministers (1960–Present)

An end-to-end data analytics project that combines India's nominal GDP, real GDP and population growth with the prime minister in office each year. Data is cleaned in Python, stored in PostgreSQL, transformed with SQL window functions and presented in an interactive Power BI dashboard.

A full write-up is in `India_Economic_Project_Report.pdf`.

## Dashboard

The Power BI report (`India_economic.pbix`, exported as `India_economic.pdf`) is a single dark-themed page with:

| Visual | Type | Shows |
|---|---|---|
| Prime Ministers | Slicer | Filter the page by prime minister |
| Year | Slicer | Filter the page by year |
| Count of Year by Name | Pie chart | Years in office per prime minister |
| Population Change by Year | Line chart | Annual population growth |
| GDP change | Line chart | Year-on-year nominal and real GDP growth |
| GDP by year | Stacked area chart | Nominal and real GDP levels |

## Project structure

```
.
├── GDP.csv                              # Raw economic data (1960–2025)
├── indian_pm_by_year_1960_2026.csv      # Prime minister for each calendar year
├── data_work.py                         # Clean data and load it into PostgreSQL
├── changes_in_gdpn.sql                  # Nominal GDP growth via LAG()
├── changes_in_gdpr.sql                  # Real GDP growth via LAG()
├── India_economic.pbix                  # Power BI report
├── India_economic.pdf                   # Dashboard exported to PDF
├── India_Economic_Project_Report.pdf    # Project report
└── README.md
```

## Data

### `GDP.csv`
66 rows, one per year from 1960 to 2025.

| Column | Description |
|---|---|
| `Year` | Calendar year |
| `GDP Nominal (Current USD)` | Nominal GDP in current US dollars |
| `GDP Real (Constant, Inflation Adjusted)` | Real GDP in constant US dollars (2015 base year: nominal equals real in 2015) |
| `Pop. Change` | Annual population growth, in percent |

Currency values use Indian digit grouping (for example `$39,56,06,71,15,772.00` is about $3.96 trillion). `data_work.py` strips the `$`, `,` and `%` characters before converting to numbers.

### `indian_pm_by_year_1960_2026.csv`
67 rows (`Name`, `Year`), one prime minister per calendar year, covering 12 people. 2026 has no matching economic data.

### Database tables

| Table | Columns |
|---|---|
| `gdpn` | `year`, `gdp(N)`, `gdp(N) change` |
| `gdpr` | `year`, `gdp(r)`, `gdp(r) change` |
| `pop_change` | `year`, `pop change` |

Growth columns are fractions (0.052 = 5.2%); `pop change` is in percent points (0.89 = 0.89%).

> **Source:** the original source of `GDP.csv` is not recorded in this repository. Add it here (provider, download date, units) before sharing.

## Pipeline

```
CSV files  →  pandas (clean)  →  PostgreSQL  →  SQL (growth rates)  →  Power BI
```

1. **Clean:** `data_work.py` renames columns, removes currency and percent symbols, converts to floats, sorts by year and computes year-on-year change with `pct_change()`.
2. **Load:** the script writes `gdpn`, `gdpr` and `pop_change` to the `india_economic` PostgreSQL database with `to_sql(..., if_exists="replace")`.
3. **Transform:** the two SQL scripts recompute the growth columns using a CTE and `LAG()` over `year`.
4. **Visualise:** Power BI reads the three tables plus the prime minister CSV, and the slicers filter all visuals by year and prime minister.

## Getting started

### Requirements
- Python 3.9+ with `pandas`, `sqlalchemy` and `psycopg2-binary`
- PostgreSQL (the report expects `localhost:5432`)
- Power BI Desktop (Windows)

```bash
pip install pandas sqlalchemy psycopg2-binary
```

### 1. Create the database
```sql
CREATE DATABASE india_economic;
```

### 2. Configure credentials
`data_work.py` currently has the database username and password written directly in the file. Move them out before sharing the project, for example:

```python
import os
username = os.environ["PG_USER"]
password = os.environ["PG_PASSWORD"]
host     = os.getenv("PG_HOST", "localhost")
port     = os.getenv("PG_PORT", "5432")
database = os.getenv("PG_DATABASE", "india_economic")
```

### 3. Load the data
Run from the folder containing `GDP.csv`:

```bash
python data_work.py
```

### 4. Recalculate growth in SQL (optional)
Run `changes_in_gdpn.sql` and `changes_in_gdpr.sql` in your SQL client (psql, pgAdmin, DBeaver). They give the same values pandas already stored, so this step is only needed if you want the database to be the source of truth.

### 5. Open the dashboard
Open `India_economic.pbix` in Power BI Desktop. If the data sources have moved, update the PostgreSQL connection and the path to `indian_pm_by_year_1960_2026.csv` under **Transform data → Data source settings**, then choose **Refresh**.

## Key results

| Metric | Value |
|---|---|
| Real GDP, 1960 → 2025 | $136B → $3.69T (about 27x) |
| Real GDP CAGR | 5.2% |
| Nominal GDP CAGR (USD) | 7.5% |
| Years of negative real growth | 5 of 65 (1965, 1966, 1972, 1979, 2020) |
| Population growth | 2.43% (1961) → 0.89% (2025); low of 0.79% in 2022 |

## Known issues and limitations

**Code**
- `data_work.py` renames `Year` to `year` and then calls `sort_values(by=["Year"])`, which raises a `KeyError`. Change it to `by=["year"]`.
- Growth is calculated twice (pandas and SQL) with identical results. Keep one.
- Column names such as `"gdp(N)"` need quoting in SQL. `snake_case` names (for example `gdp_nominal`) would be easier to use.

**Dashboard**
- "GDP by year" is a *stacked* area chart, so its top line is nominal plus real GDP (about $7.65T in 2025). Use a line or unstacked area chart.
- Growth rates and population change are in different units (fraction vs percent points).
- Visuals use *Sum* on rates; use average or CAGR measures if several years are selected.

**Data**
- Each calendar year is assigned to one prime minister, so mid-year changes of government and short or interim governments are not represented.
- Population growth is exactly 0.89% for 2023–2025, which suggests an estimate.
- Nominal GDP is in US dollars, so it is affected by exchange-rate movements as well as output. Real growth is the better basis for comparing periods.
- Averages by prime minister describe what happened in each period and do not show that a government caused it.

## Possible extensions
- Add inflation, the INR/USD exchange rate and GDP in rupees
- Add a population-level series to calculate GDP per capita
- Use start and end dates for each prime minister's tenure
- Add 2026 data when it becomes available
