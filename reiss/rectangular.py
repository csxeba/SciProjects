import os

import numpy as np
import cv2
from matplotlib import patches
from matplotlib import pyplot as plt

from SciProjects.reiss.util import get_image


SCALE = 1. / 26.875

projectroot = "/home/csa/Rizs/"
binpath = projectroot + "bin/"


def fit_rect(prp):
    xy = np.argwhere(prp.image)
    cxy, (h, w), theta = cv2.minAreaRect(xy)
    # print("h:", h*SCALE, "w:", w*SCALE, "R:", h/w)
    # ell = patches.Ellipse(cxy, h, w, theta)
    # ell.set_facecolor("none")
    # ell.set_edgecolor("black")
    # plt.scatter(*xy.T, alpha=0.5)
    # plt.scatter(*cxy, marker="x")
    # ax = plt.gca()
    # ax.add_patch(ell)
    # plt.show()
    h, w = max((h, w)), min((h, w))
    return h*SCALE, w*SCALE, h/w


flz = sorted(os.listdir(binpath), reverse=True)
nfl = len(flz)
strln = len(str(nfl))
header = "SAMPLE\tPROP\tPRPAREA\tL\tW\tR\n"
results = []
for i, pngfl in enumerate(flz, start=1):
    prps, flnm, dirz = get_image(binpath + pngfl)
    for j, prp in enumerate((p for p in prps if 100 < p.area < 15000), start=1):
        h, w, r = fit_rect(prp)
        results.append([pngfl[:-4], j, prp.area, h, w, r])

chain = header + "\n".join("\t".join(map(str, line)) for line in results)
with open(projectroot + "measurement.csv", "w") as handle:
    handle.write(chain)

sumchain = "MINTA\tL_ÁTLAG\tL_SZÓR\tR_ÁTLAG\tR_SZÓR\tN\t%TÖRM\n"
results = np.array(results)
smpls = np.sort(np.unique(results[:, 0]))
for smpl in smpls:
    this = results[results[:, 0] == smpl]  # type: np.ndarray
    L, R = this[:, (3, 5)].astype(float).T
    mn = L.mean()

    sumchain += "\t".join(map(str, (
        smpl, mn, L.std(), R.mean(), R.std(),
        len(this), L[L <= mn*0.75].sum() / len(this)
    ))) + "\n"

with open(projectroot + "summary.csv", "w") as handle:
    handle.write(sumchain)
