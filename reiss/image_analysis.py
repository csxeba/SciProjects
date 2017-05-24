import numpy as np

from matplotlib import pyplot as plt
from reiss.util import get_image

from skimage import measure, feature


def calc_eigenvectors(image):
    for prp in measure.regionprops(image):
        XY = np.argwhere(prp.image)
        mxy = XY.mean(axis=0)
        sxy = XY.std(axis=0)
        iXY = (XY - mxy) / sxy
        cv = np.cov(iXY.T)
        eva, evc = np.linalg.eig(cv)
        evx, evy = evc.T * sxy
        mx, my = mxy
        plt.scatter(XY[:, 0], XY[:, 1])
        plt.arrow(mx, my, evx[0], evx[1])
        plt.arrow(mx, my, evy[0], evy[1])
        plt.show()


def feret(image):
    for prp in (p for p in measure.regionprops(image) if p.area > 100):
        edge = feature.canny(prp.image)
        plt.imshow(edge)
        plt.show()


img = get_image()
img = measure.label(img)

feret(img)
