import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from alice_weight import projectroot

PROJECT_ROOT = "/data/Megosztott/Dokumentumok/SciProjects/Project_AliceWeight/"

ADATA = "alice_weight.xlsx"
BDATA = "benedict.xlsx"

adf = pd.read_excel(PROJECT_ROOT + ADATA)
bdf = pd.read_excel(PROJECT_ROOT + BDATA)

adf["tdelta"] = (adf.date - adf.date[0]).values.astype(int)
bdf["tdelta"] = (bdf.date - bdf.date[0]).values.astype(int)

aX = adf.tdelta.values
aY = adf.grams.values

bX = bdf.tdelta.values
bY = bdf.grams.values

plt.plot(aX, aY, color="magenta", label="Alíz")
plt.scatter(aX, aY, c="magenta")
plt.plot(bX, bY, color="blue", label="Benedek")
plt.scatter(bX, bY, c="blue")
plt.grid(True)
plt.show()
