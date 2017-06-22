import numpy as np
from matplotlib import pyplot as plt

from csxdata.utilities.vectorops import split_by_categories

from SciProjects.riskanalyze.utils import pull_data


# data header: RENDSZAM	SZOLGHELY	DATUM	HELY	MINTA	MEGF
xy, data = pull_data()
date, valid = data[:, 2], data[:, 5]

xy = xy.astype(float)

sxy = split_by_categories(valid, xy)

date = np.array([s.replace(".", "-") for s in date], dtype="datetime64[D]")
dmin, dmax = date.min(), date.max()
tdelta = (date - date.min()).astype(int)
alphas = np.ones_like(tdelta) * (tdelta / tdelta.max())
red_rgba = np.zeros((alphas.size, 4))
red_rgba[:, 2] = 1
red_rgba[:, 3] = alphas

xmin, ymin = xy.min(axis=0)
xmax, ymax = xy.max(axis=0)
plt.scatter(*xy.T, c=red_rgba)
# plt.scatter(*sxy["1"].T, color=date, s=3)
# plt.scatter(*sxy["0"].T, color="red", s=3)
plt.show()
