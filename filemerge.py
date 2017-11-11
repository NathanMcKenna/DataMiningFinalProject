import pandas as pd

a = pd.read_csv("2016.csv")
b = pd.read_csv("countries.csv")

final = a.merge(b, on="Country", how="outer")
final.to_csv("finalmerge.csv", index=False)
