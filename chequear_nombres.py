import pandas as pd

df = pd.read_csv("partidos_stats_pulido.csv")
print(df.columns.tolist())
print(df.head())