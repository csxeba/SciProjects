import numpy as np
from matplotlib import pyplot as plt

from csxdata.stats import manova
from csxdata.visual import Plotter2D
from csxdata.utilities.highlevel import transform

from SciProjects.sophie import pull_data, axtitles


X_C, Y_C, DHI, D13C, CCode = pull_data("03GEO_pure.csv")

ingoes = np.stack((DHI, D13C), axis=1)

tX = transform(ingoes, 1, False, "lda", CCode)
F, p = manova(tX, CCode)

ttl = (r"2 $\sigma$ (kb. 95%), országokra illesztett konfidencia ellipszisek",
       "LDA + ANOVA: F = {:.2f}, p = {:.2f}, az eltérés {}szignifikáns"
       .format(F, p, ("nem " if p > 0.05 else "")))
axlb = (axtitles["DHI"], axtitles["D13C"])

plot = Plotter2D(plt.figure(), ingoes, CCode, title="\n".join(ttl), axlabels=axlb)
plot.split_scatter(center=True, sigma=2, alpha=0.5)

plt.show()
