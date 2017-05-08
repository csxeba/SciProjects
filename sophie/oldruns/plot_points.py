import numpy as np
from matplotlib import pyplot as plt

from csxdata.utilities.parsers import parse_csv
from csxdata.utilities.vectorops import discard_NaN_rows
from csxdata.utilities.highlevel import plot

from SciProjects.sophie import projectroot


X, Y, head = parse_csv(projectroot + "01GEO.csv",
                       indeps=4, headers=1, decimal=True)

y_coord = Y[:, -1].astype(float)
countries = Y[:, 0]
DHI, D13C = X.T

plot(np.stack((y_coord, DHI), axis=1), countries, axlabels=["Y", "DHI"])
plotme, c2 = discard_NaN_rows(np.stack((y_coord, D13C), axis=1), countries)
plot(plotme, c2, ["Y", "D13C"])

fig, axarr = plt.subplots(2)
axarr[0].scatter(y_coord, DHI, color="red", marker=".")
axarr[0].set_xlabel(r"$(D/H)_I$")
axarr[1].scatter(y_coord, D13C, color="red", marker=".")
axarr[1].set_xlabel(r"$\delta^13C$")
axarr[0].set_ylabel("Y")
axarr[1].set_ylabel("Y")
plt.tight_layout()
plt.show()
