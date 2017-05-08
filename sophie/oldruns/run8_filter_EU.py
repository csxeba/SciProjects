import numpy as np
from scipy import stats
from matplotlib import pyplot as plt

from csxdata.visual import Plotter2D
from csxdata.utilities.vectorops import discard_NaN_rows
from csxdata.stats.inspection import category_frequencies

from SciProjects.sophie import pull_data, axtitles

X_C, Y_C, DHI, D13C, CCode = pull_data("04GEO_eu.csv")

DHI, Y_C, CCode = discard_NaN_rows(DHI, Y_C, CCode)
category_frequencies(CCode)
R, p = stats.spearmanr(DHI, Y_C)

line = np.polyfit(Y_C, DHI, 1)
line = np.poly1d(line)

ttl = ("Korreláció $(D/H)_I$ és az egyenlítőtől való távolság között Európában",
       f"Spearman-korreláció: R = {R:.2f}, p = {p:.2f}, {('nem' if p > 0.05 else '')}szignifikáns")
axttl = ["Egyenlítőtől való távolság", axtitles["DHI"]]

plotter = Plotter2D(plt.figure(), np.stack((Y_C, DHI), axis=1),
                    CCode, title="\n".join(ttl), axlabels=axttl)
plotter.split_scatter(center=True, sigma=2, alpha=0.5)
plotter.add_trendline("r", lw=1)
plotter.add_legend(plt)
plt.show()
