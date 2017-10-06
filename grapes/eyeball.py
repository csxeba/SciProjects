from csxdata import CData
from csxdata.utilities.highlevel import plot, transform
from SciProjects.generic import paths

FEATURE = "evjarat"

grapes = CData(*paths["grapes"], feature=FEATURE, cross_val=0, lower=True)
X, Y = grapes._learning, grapes.lindeps


def plot_raw():
    plot(X[:, ::2], Y, ["DH1", "D13C"], 1)


def plot_pca():
    lX = transform(X, factors=2, get_model=False, method="pca")
    plot(lX, Y, ["PC1", "PC2"], 1)


def plot_lda():
    lX = transform(X, factors=2, get_model=False, method="lda", y=Y)
    plot(lX, Y, ["LD1", "LD2"], 1)


def plot_ica():
    lX = transform(X, factors=2, get_model=False, method="ica")
    plot(lX, Y, ["IC1", "IC2"], 1)


# def plot_ae():
#     lX = transform(X, 2, False, "ae", y=Y)
#     plot(lX, Y, ["F01", "F02"], 1)


if __name__ == '__main__':
    for f in [func for name, func in globals().items() if name[:5] == "plot_"]:
        f()
