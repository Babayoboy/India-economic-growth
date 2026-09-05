import pandas as pd

dataframe = pd.read_csv("GDP.csv")

dataframe = dataframe.rename(columns = {"GDP Nominal (Current USD)": "GDP(N)", "GDP Real (Constant, Inflation Adjusted)": "GDP(R)"})
print(dataframe)

dataframe[["GDP(N)", "GDP(R)", "Pop. Change"]] =  dataframe[["GDP(N)", "GDP(R)", "Pop. Change"]].replace({r"\$":'', ',':'', '%':''}, regex=True).astype(float)
dataframe.sort_values(by=["Year"], ascending=True, inplace=True)
print(dataframe)
dataframe_change = dataframe[["GDP(N)", "GDP(R)"]].pct_change()
dataframe[["GDP(N) change", "GDP(R) change"]] = dataframe_change
print(dataframe)
