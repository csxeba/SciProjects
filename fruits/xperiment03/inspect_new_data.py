import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
from matplotlib import mlab

from csxdata.stats.normality import full
from SciProjects.fruits import projectroot


def histogram(X, name, nbins=30):
    plt.clf()
    fig, (plotax, histax) = plt.subplots(1, 2, figsize=(12, 6))
    mean, std = X.mean(), X.std()
    n, bins, patches = histax.hist(X, nbins, normed=1, facecolor="green", edgecolor="black", alpha=0.75)
    y1 = mlab.normpdf(bins, mean, std)
    histax.plot(bins, y1, "--")
    histax.set_title(f"Hist of {name}")
    histax.grid(True)

    plotax.plot(np.arange(1, len(X)+1), sorted(X))
    plotax.set_title(f"{name}")
    plotax.grid(True)
    plt.tight_layout()
    plt.savefig(projectroot + f"{name}.png")
    # plt.show()


isotope = ["DH1", "DH2", "D13C"]
volatile = ["METOH", "ACALD", "ETAC", "ACETAL", "2BUT",
            "1PROP", "2M1P", "1BUT", "2M1B", "3M1B"]

data = pd.read_excel(projectroot + "Gyümölcs_adatbázis_összesített.xlsx", header=0, index_col=0)

valid = data[isotope + volatile].dropna()
isoX = valid[isotope].as_matrix()
volX = valid[volatile].as_matrix()
volX /= volX.max(axis=0)
np.log(volX+1e-5, out=volX)

full(isoX, names=isotope)
full(volX, names=volatile)

for X, volnm in zip(volX.T, volatile):
    print(f"MIN: {X.min()} MAX: {X.max()}")
    histogram(X, volnm)

for X, isonm in zip(isoX.T, isotope):
    print(f"MIN: {X.min()} MAX: {X.max()}")
    histogram(X, isonm)
