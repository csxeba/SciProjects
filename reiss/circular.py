import os

import numpy as np
from scipy import spatial
from sklearn import decomposition
from matplotlib import patches
from matplotlib import pyplot as plt

from SciProjects.reiss.util import get_image


SCALE = 1. / 26.875

projectroot = "/home/csa/Rizs/"
binpath = projectroot + "bin/"


def do_eig(prop):
    X = np.argwhere(prop.image)
    cov = np.cov(X.T)
    E, V = np.linalg.eigh(cov)
    S = np.sort(np.sqrt(E))
    w, h = S * 2 * 2 * SCALE
    return h, w, h / w


def do_svd(prop):
    X = np.argwhere(prop.image)
    S = np.linalg.svd(X, compute_uv=False)  # type: np.ndarray
    h, w = S * 2 * 2 * SCALE
    return h, w, h / w


def fit_circle(prop):
    xy = np.argwhere(prop.image)
    pca = decomposition.PCA(2, whiten=False).fit(xy)
    txy = pca.transform(xy)
    mxy = txy.max(axis=0)
    txy /= mxy
    ch = spatial.ConvexHull(txy)
    r = ch.area / ch.perim
    plt.scatter(*txy.T)
    plt.show()


def combine_em(prop):
    xy = np.argwhere(prop.image)
    mxy = np.mean(xy, axis=0)

    cov = np.cov(xy.T)
    E, V = np.linalg.eigh(cov)
    S = np.sqrt(E)

    w = S[0] * 2 * 2
    h = S[1] * 2 * 2

    print(h*SCALE, w*SCALE, S.max() / S.min(), sep=";")

    theta = np.degrees(np.arctan(V[0, 1]))
    ell = patches.Ellipse(mxy, w, h, theta)
    ell.set_edgecolor("black")
    ell.set_facecolor("none")
    fig, ax = plt.subplots(1, 2)
    ax[0].scatter(*xy.T, alpha=0.5)
    ax[0].add_patch(ell)
    ax[1].imshow(prop.image)
    plt.suptitle("R = " + str(S.max() / S.min()))
    plt.show()

    return h*SCALE, w*SCALE, S.max() / S.min()


flz = os.listdir(binpath)
nfl = len(flz)
strln = len(str(nfl))
chain = "SAMPLE\tPROP\tPRPAREA\tL\tW\tR\n"
for i, pngfl in enumerate(flz, start=1):
    # print(f"\r{i:>{strln}}/{nfl} - {pngfl}", end="")
    prps, flnm, dirz = get_image(binpath + pngfl)
    for j, prp in enumerate((p for p in prps if 100 < p.area < 15000), start=1):
        h, w, r = combine_em(prp)
        chain += "\t".join(map(str, (pngfl, j, prp.area, h, w, r))) + "\n"

with open(projectroot + "measurement.csv", "w") as handle:
    handle.write(chain)
