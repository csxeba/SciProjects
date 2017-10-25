from itertools import combinations_with_replacement

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from csxdata.utilities.vectorop import split_by_categories

from SciProjects.matt import projectroot


def plotsingle(ax, X1, X2, Y, name1, name2, coord):
    color = {"Alma": "red", "Kajszi": "orange", "Málna": "magenta"}
    args = split_by_categories(Y)
    for cat in np.unique(Y):
        ax.scatter(X1[args[cat]], X2[args[cat]], marker=".", color=color[cat])
    line = np.poly1d(np.polyfit(X1, X2, deg=1))
    ax.plot(X1, line(X1), "b-", linewidth=1)
    if not coord[0]:
        ax.set_title(name2)
    if not coord[1]:
        ax.set_ylabel(name1)
    ax.grid(True)


df = pd.read_excel(projectroot + "adat.xlsx", header=0)

fig, axarr = plt.subplots(5, 5)

for i, col1, axrow in zip(range(5), df.columns[1:], axarr):
    for j, col2, ax in zip(range(5), df.columns[1:], axrow):
        plotsingle(ax, df[col1], df[col2], df["GYUM"], col1, col2, (i, j))

plt.tight_layout()
plt.show()
