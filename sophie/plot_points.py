import numpy as np
from matplotlib import pyplot as plt

from csxdata.utilities.parsers import parse_csv
from csxdata.utilities.vectorops import argfilter

from SciProjects.sophie import projectroot


X, Y, head = parse_csv(projectroot + "01GEO.csv",
                       indeps=4, headers=1, decimal=True)

y_coord = Y[:, -1]
countries = Y[:, 1]
DHI, D13C = X.T
plt.scatter(y_coord, D13C)
plt.show()
