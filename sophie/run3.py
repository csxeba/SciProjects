import numpy as np

from csxdata.utilities.parsers import parse_csv
from csxdata.utilities.vectorops import discard_NaN_rows, discard_lowNs
from csxdata.utilities.highlevel import plot
from csxdata.stats.inspection import category_frequencies

from SciProjects.sophie import projectroot


def plotit(what):
    if what == "DHI":
        plotme = np.stack((DHI, Y_C), axis=1)
    else:
        plotme = np.stack((D13C, Y_C), axis=1)
    plotmeX, plotmeY = discard_NaN_rows(plotme, country_codes)
    category_frequencies(plotmeY)
    plot(plotmeX, plotmeY, axlabels=[what, "Y"])


def plotit3d():
    plotme = np.stack((DHI, D13C, Y_C), axis=1)
    plotmeX, plotmeY = discard_NaN_rows(plotme, country_codes)
    category_frequencies(plotmeY)
    plot(plotmeX, plotmeY, axlabels=["DHI", "D13C", "Y"])

X, Y, head = parse_csv(projectroot + "02GEO.csv", indeps=3, headers=1, dehungarize=True, sep=",")
coords, X = X[:, :2], X[:, (2, 4)]
DHI, D13C = X.T
X_C, Y_C = coords.T
country_codes = Y[:, 1]

plotit("DHI")
plotit("D13C")
plotit3d()
