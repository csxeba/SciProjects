from datetime import datetime, timedelta
from collections import deque

import numpy as np
import pandas as pd

from SciProjects.rich import projectroot


df = pd.read_excel(projectroot + "Rdata.xlsx")
df["Dátum"] = pd.to_datetime(df["Dátum"], format="%Y.%m.%d.")
print(df.dtypes)

stocks = np.unique(df["Név"])

dr = pd.date_range("2015-01-01", "2017-09-28")

output = np.zeros((len(dr), len(stocks)))

times = deque()
ETA = 0.

lstck = len(stocks)
ldates = len(dr)
lldates = len(str(ldates))
globstart = datetime.now()
for i, stock in enumerate(sorted(stocks)):

    start = datetime.now()
    print(f"Doing {i+1}/{lstck}: {stock})")
    print(f"ETA: {ETA // 60} minutes, finish @ {globstart + timedelta(seconds=ETA)}")

    for j, day in enumerate(dr):
        print(f"\rDate: {j:>{lldates}}/{ldates}", end="")
        day_stimmt = df["Dátum"] == day
        name_stimmt = df["Név"] == stock
        stimmt = df.loc[np.logical_and(day_stimmt, name_stimmt)]["Záróár"]  # type: pd.Series
        lns = len(stimmt)
        assert lns <= 1, f"{stock} @ {day} N = {lns}"
        output[j, i] = stimmt.as_matrix()[0] if lns else np.nan

    print()
    times.append((datetime.now() - start).seconds)
    ETA = ((sum(times) / len(times)) * lstck)

ndf = pd.DataFrame(output, index=dr, columns=sorted(stocks))
ndf.to_excel(projectroot + "output.xlsx")
