import numpy as np

from csxdata.stats.inspection import category_frequencies
from csxdata.utilities.highlevel import plot
from csxdata.utilities.parser import parse_csv
from csxdata.utilities.vectorop import drop_lowNs, dropna

from SciProjects.sophie import projectroot

X, Y, head = parse_csv(projectroot + "01GEO.csv",
                       indeps=4, headers=1, decimal=True)

y_coord = Y[:, -1].astype(float)
categ = Y[:, 0]
DHI, D13C = X.T
plotme = np.stack((DHI, D13C, y_coord), axis=1)
plotme, categ = dropna(plotme, categ)
category_frequencies(categ)
plot(plotme, axlabels=["DHI", "D13C", "Y"])
