import pandas as pd

dataframe = pd.read_csv("GDP.csv")

dataframe = dataframe.rename(columns = {"GDP Nominal (Current USD)": "GDP(N)", "GDP Real (Constant, Inflation Adjusted)": "GDP(R)"})
print(dataframe)

dataframe[["GDP(N)", "GDP(R)"]] =  dataframe[["GDP(N)", "GDP(R)"]].replace({r"\$":''}, regex=True)
print(dataframe)
dataframe_change = to_numeric(dataframe.pct_change())
print(dataframe_change)
