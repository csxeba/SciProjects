import numpy as np

from csxdata.utilities.vectorops import discard_lowNs
from csxdata.utilities.parsers import parse_csv
from csxdata.utilities.highlevel import plot, transform

from SciProjects.sophie import projectroot


def plot_projection(projection):
    nX = np.stack((X[:, 0], X[:, 1], Y_C), axis=1)
    fX, fY = discard_lowNs(nX, country_codes)
    fX, fY_C = fX[:, :2], fX[:, -1]
    tX = transform(fX, factors=1, get_model=False, method=projection, y=fY).ravel()
    plot(np.stack((fY_C, tX), axis=1), fY, axlabels=["Y", projection.upper()])

X, Y, head = parse_csv(projectroot + "03GEO_pure.csv", headers=1, indeps=3,
                       dehungarize=True, sep=",")

coords, X = X[:, :2], X[:, (2, 4)]
X_C, Y_C = coords.T
country_codes = Y[:, 1]

plot_projection("pca")
plot_projection("lda")
