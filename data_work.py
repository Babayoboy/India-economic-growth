import pandas as pd
from sqlalchemy import create_engine

dataframe = pd.read_csv("GDP.csv")

dataframe = dataframe.rename(columns = {"GDP Nominal (Current USD)": "gdp(N)", "GDP Real (Constant, Inflation Adjusted)": "gdp(r)", "Pop. Change": "pop change", "Year": "year"})

dataframe[["gdp(N)", "gdp(r)", "pop change"]] =  dataframe[["gdp(N)", "gdp(r)", "pop change"]].replace({r"\$":'', ',':'', '%':''}, regex=True).astype(float)

dataframe.sort_values(by=["Year"], ascending=True, inplace=True)

dataframe_change = dataframe[["gdp(N)", "gdp(r)"]].pct_change()

dataframe[["gdp(N) change", "gdp(r) change"]] = dataframe_change

print(dataframe)

username = "joshi"
password = "2096"
host = "localhost"
port = "5432"
database = "india_economic"

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

table_name1 = "gdpn"
table_name2 = "gdpr"
table_name3 = "pop_change"

dataframe[["year", "gdp(N)", "gdp(N) change"]].to_sql(table_name1, engine, if_exists="replace", index=False)
dataframe[["year", "gdp(r)", "gdp(r) change"]].to_sql(table_name2, engine, if_exists="replace", index=False)
dataframe[["year", "pop change"]].to_sql(table_name3, engine, if_exists="replace", index=False)

print(f"Data successfully loaded into table '{table_name1}' in database '{database}'.")
print(f"Data successfully loaded into table '{table_name2}' in database '{database}'.")
print(f"Data successfully loaded into table '{table_name3}' in database '{database}'.")
