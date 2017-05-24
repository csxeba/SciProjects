import numpy as np
from scipy import spatial
from sklearn import decomposition
from skimage import measure
from matplotlib import pyplot as plt

from SciProjects.reiss.util import get_image


def do_svd(prop):
    xy = np.argwhere(prop.image)
    S = np.linalg.svd(xy, compute_uv=False)
    print(S[0] / S[1])
    fig, ax = plt.subplots(1, 2)
    ax[0].scatter(*xy.T)
    ax[1].imshow(prop.image)
    plt.suptitle("R = " + str(S[0] / S[1]))
    plt.show()


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


img = get_image()
img = measure.label(img)

prpstream = (prp for prp in measure.regionprops(img) if prp.area > 10)
for prp in prpstream:
    do_svd(prp)
