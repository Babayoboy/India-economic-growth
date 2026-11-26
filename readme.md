# India's Economic & Demographic Journey Across Prime Ministers (1960–Present)

An end-to-end data analytics project that combines India's nominal GDP, real GDP, GDP per capita and population growth with the prime minister in office each year. Data is cleaned in Python, stored in PostgreSQL, transformed with SQL window functions and presented in an interactive Power BI dashboard.

A full write-up is in `India_Economic_Project_Report.pdf`.

## Dashboard

The Power BI report (`India_economic.pbix`, exported as `India_economic.pdf`) is a single dark-themed page with seven visuals:

| Visual | Type | Shows |
|---|---|---|
| Prime Ministers | Slicer | Filter the page by prime minister |
| Year | Slicer | Filter the page by year |
| Year in power by Prime Minister | Pie chart | Years in office per prime minister |
| Population Change by Year | Line chart | Annual population growth |
| GDP change | Line chart | Year-on-year nominal and real GDP growth |
| GDP by year | Line chart | Nominal and real GDP levels |
| GDP per capita by Year | Line chart | Nominal and real GDP per person |

## Project structure

```
.
├── GDP.csv                              # Raw economic data (1960–2025)
├── gdp_per_capita.csv                   # Nominal and real GDP per person (1960–2025)
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

### `gdp_per_capita.csv`
66 rows, one per year from 1960 to 2025.

| Column | Description |
|---|---|
| `year` | Calendar year |
| `percapgdpn` | Nominal GDP per person, current US dollars |
| `percapgdpr` | Real GDP per person, constant 2015 US dollars (equals `percapgdpn` in 2015) |

Values are plain numbers (no symbols). The file is read directly by Power BI and is not processed by `data_work.py`. Dividing `GDP.csv` by these values implies a population series whose growth matches `Pop. Change` to within 0.01 points.

### `indian_pm_by_year_1960_2026.csv`
67 rows (`Name`, `Year`), one prime minister per calendar year, covering 12 people. 2026 has no matching economic data.

### Database tables

| Table | Columns |
|---|---|
| `gdpn` | `year`, `gdp(N)`, `gdp(N) change` |
| `gdpr` | `year`, `gdp(r)`, `gdp(r) change` |
| `pop_change` | `year`, `pop change` |

Growth columns are fractions (0.052 = 5.2%); `pop change` is in percent points (0.89 = 0.89%). GDP per capita is not stored in PostgreSQL.

> **Source:** the original sources of `GDP.csv` and `gdp_per_capita.csv` are not recorded in this repository. Add them here (provider, download date, units, licence) before sharing.

## Pipeline

```
GDP.csv  →  pandas (clean)  →  PostgreSQL  →  SQL (growth rates)  ┐
gdp_per_capita.csv  ───────────────────────────────────────────────┼→  Power BI
indian_pm_by_year_1960_2026.csv  ──────────────────────────────────┘
```

1. **Clean:** `data_work.py` renames columns, removes currency and percent symbols, converts to floats, sorts by year and computes year-on-year change with `pct_change()`.
2. **Load:** the script writes `gdpn`, `gdpr` and `pop_change` to the `india_economic` PostgreSQL database with `to_sql(..., if_exists="replace")`.
3. **Transform:** the two SQL scripts recompute the growth columns using a CTE and `LAG()` over `year`.
4. **Visualise:** Power BI reads the three PostgreSQL tables plus the two CSV files (prime ministers and GDP per capita), and the slicers filter all visuals by year and prime minister.

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
`data_work.py` currently has the database username and password written directly in the file. Move them out before sharing the project, and change the password that has already been shared, for example:

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
Open `India_economic.pbix` in Power BI Desktop. If the data sources have moved, update the PostgreSQL connection and the paths to `indian_pm_by_year_1960_2026.csv` and `gdp_per_capita.csv` under **Transform data → Data source settings**, then choose **Refresh**.

## Key results

| Metric | Value |
|---|---|
| Real GDP, 1960 → 2025 | $136B → $3.69T (about 27x) |
| Real GDP CAGR | 5.2% |
| Nominal GDP CAGR (USD) | 7.5% |
| Real GDP per capita, 1960 → 2025 | $313 → $2,523 (about 8x) |
| Real GDP per capita CAGR | 3.3% |
| Nominal GDP per capita, 1960 → 2025 | $85 → $2,702 (about 32x, 5.5% a year) |
| Years of negative real growth | 5 of 65 (1965, 1966, 1972, 1979, 2020) |
| Years of negative real per-capita growth | 9 of 65 |
| Population growth | 2.43% (1961) → 0.89% (2025); low of 0.79% in 2022 |

Real GDP per capita grew 0.6% a year in the 1970s and between 3.3% and 5.3% a year in every decade since the 1980s (2020s so far: 4.7%).

## Known issues and limitations

**Code**
- `data_work.py` renames `Year` to `year` and then calls `sort_values(by=["Year"])`, which raises a `KeyError`. Change it to `by=["year"]`.
- Growth is calculated twice (pandas and SQL) with identical results. Keep one.
- Column names such as `"gdp(N)"` need quoting in SQL. `snake_case` names (for example `gdp_nominal`) would be easier to use.
- GDP per capita sits outside the pipeline: it is read straight from CSV and the population series behind it is not in the repository.

**Dashboard**
- **The "GDP per capita by Year" legend is swapped.** The series named "Nominal" plots `percapgdpr` (real) and the series named "Real" plots `percapgdpn` (nominal). Swap the two names in Power BI.
- The same chart's title and subtitle read "GDP per capta" (should be "capita"), and its axis has no dollar sign or note on current versus constant dollars.
- Growth rates and population change are in different units (fraction vs percent points).
- Visuals use *Sum* on rates; use average or CAGR measures if several years are selected.
- The "Year in power" pie shows tenure length, not performance, and counts 13 years for Modi because of the 2026 row (12 years of data).

**Data**
- Each calendar year is assigned to one prime minister, so mid-year changes of government and short or interim governments are not represented.
- Population growth is exactly 0.89% for 2023–2025, which suggests an estimate.
- Nominal GDP is in US dollars, so it is affected by exchange-rate movements as well as output. Real growth is the better basis for comparing periods.
- GDP per capita is a national average and says nothing about how income is distributed.
- Averages by prime minister describe what happened in each period and do not show that a government caused it.

## Possible extensions
- Add inflation, the INR/USD exchange rate and GDP in rupees
- Load GDP per capita (and its population series) into PostgreSQL and calculate its growth in SQL
- Use start and end dates for each prime minister's tenure
- Add 2026 data when it becomes available
