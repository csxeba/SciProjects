import numpy as np
import matplotlib.pyplot as plt

from project_fruits.util import pull_data, pull_fruits_data, dummycoding


ELLIPSE = True
ELLIPSE_SIGMA = 2

axlb = {
    "raw": ("DH1", "DH2", "D13C"),
    "log": ("logDH1", "logDH2", "D13C"),
    "sqrt": ("sqrtDH1", "sqrtDH2", "D13C"),
    "sigm": ("sigmDH1", "D13C"),
    "pca": ("PC01", "PC02", "PC03"),
    "ica": ("IC01", "IC02", "IC03"),
    "lda": ("LD01", "LD02", "LD03"),
    "sinu": ("sinDH1", "sinDH2", "D13C"),
    "fft": ("fftDH1", "fftDH2", "D13C"),
    "ae": ("AE1", "AE2", "AE3")
}


def get_markers():
    colors = ["red", "blue", "green", "orange", "black"]
    markers = ["o", 7, "D", "x"]
    mrk = []
    for m in markers:
        for c in colors:
            mrk.append((c, m))
    return mrk


def split_by_categories(independent, dependent):
    categ = sorted(list(set(dependent)))
    bycat = []
    for cat in categ:
        eq = np.equal(dependent, cat)
        args = np.ravel(np.argwhere(eq))
        bycat.append(independent[args])
    return dict(zip(categ, bycat))


def plot(points, dependents, axlabels):

    fig = plt.figure()

    def construct_confidence_ellipse(x, y):
        from matplotlib.patches import Ellipse

        vals, vecs = np.linalg.eig(np.cov(x, y))

        w = np.sqrt(vals[0]) * ELLIPSE_SIGMA * 2
        h = np.sqrt(vals[1]) * ELLIPSE_SIGMA * 2
        theta = np.degrees(np.arctan2(*vecs[:, 0][::-1]))

        ell = Ellipse(xy=(np.mean(x), np.mean(y)),
                      width=w, height=h, angle=theta)
        ell.set_facecolor("none")
        ell.set_edgecolor(color)
        ax.add_artist(ell)

    def scat3d(Xs):
        x, y, z = Xs.T
        plt.scatter(x=x, y=y, zs=z, zdir="z", c=color,
                    marker=marker, label=translate(ct))

    def scat2d(Xs):
        x, y = Xs.T

        if ELLIPSE:
            construct_confidence_ellipse(x, y)

        plt.scatter(x=x, y=y, c=color, marker=marker,
                    label=translate(ct))

    if points.shape[-1] == 3:
        # noinspection PyUnresolvedReferences
        from mpl_toolkits.mplot3d import Axes3D
        mode = "3d"
        ax = fig.add_subplot(111, projection="3d")
        scat = scat3d
    else:
        mode = "2d"
        ax = fig.add_subplot(111)
        scat = scat2d

    points, dependents, translate = dummycoding(points, dependents)
    axlabels = axlabels[:int(mode[0])]

    by_categories = split_by_categories(points, dependents)
    setters = [ax.set_xlabel, ax.set_ylabel]
    if mode == "3d":
        setters.append(ax.set_zlabel)

    for st, axlb in zip(setters, axlabels):
        st(axlb)
    for ct, ctup in zip(by_categories, get_markers()):
        color, marker = ctup
        scat(by_categories[ct])

    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=0,
               ncol=7, mode="expand", borderaxespad=0.)
    plt.show()


def xperiment(transformation, tax_level, param=0, paramset="all"):
    transformation = transformation.lower()[:4]

    X, y = pull_data(absval=True, param=param, transformation=transformation, label=tax_level, paramset=paramset)
    plot(X[:, (0, 2)], y, axlabels=axlb[transformation])


def fruits_xperiment(transformation, param):
    transformation = transformation.lower()[:4]

    X, y = pull_fruits_data(transformation, param)
    plot(X, y, axlabels=axlb[transformation])


if __name__ == '__main__':
    fruits_xperiment(transformation="lda", param=2)
