import numpy as np
import pandas as pd

from csxdata.visual.progress import enumprogress

from SciProjects.rich import projectroot


df = pd.read_excel(projectroot + "Rdata.xlsx")
df["Dátum"] = pd.to_datetime(df["Dátum"], format="%Y.%m.%d.")
print(df.dtypes)

stocks = np.unique(df["Név"])

dr = pd.date_range("2015-01-01", "2017-09-28")

ndf = pd.DataFrame(
    index=dr,
    columns=["Date"] + sorted(stocks),
)

for stock in sorted(stocks):
    print("Doing", stock)

    for day in enumprogress(dr, prefix="Date: "):
        day_stimmt = df["Dátum"] == day
        name_stimmt = df["Név"] == stock
        stimmt = df.loc[np.logical_and(day_stimmt, name_stimmt)]["Záróár"]
        assert len(stimmt) <= 1, f"{stock} @ {day} N = {len(stimmt)}"
        ndf[day, stock] = stimmt

ndf.to_excel(projectroot + "Reparsed.xlsx")
