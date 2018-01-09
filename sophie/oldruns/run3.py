import numpy as np

from csxdata.utilities.parser import parse_csv
from csxdata.utilities.vectorop import dropna, drop_lowNs
from csxdata.utilities.highlevel import plot, transform
from csxdata.stats.inspection import category_frequencies

from SciProjects.sophie import projectroot


def plotit(what):
    if what == "DHI":
        plotme = np.stack((Y_C, DHI), axis=1)
    else:
        plotme = np.stack((Y_C, D13C), axis=1)
    plotmeX, plotmeY = dropna(plotme, country_codes)
    plotmeX, plotmeY = drop_lowNs(plotmeX, plotmeY, threshold=5)
    category_frequencies(plotmeY)
    plot(plotmeX, plotmeY, axlabels=["Y", what])


def plotit3d():
    plotme = np.stack((Y_C, DHI, D13C), axis=1)
    plotmeX, plotmeY = dropna(plotme, country_codes)
    category_frequencies(plotmeY)
    plot(plotmeX, plotmeY, axlabels=["Y", "DHI", "D13C"])

X, Y, head = parse_csv(projectroot + "02GEO.csv", indeps=3,
                       headers=1, dehungarize=True, sep=",")
coords, X = X[:, :2], X[:, (2, 4)]
DHI, D13C = X.T
X_C, Y_C = coords.T
country_codes = Y[:, 1]

plotit("DHI")
plotit("D13C")
plotit3d()
