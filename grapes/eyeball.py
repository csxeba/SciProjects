from csxdata.utilities.highlevel import plot, transform

from project_grapes.misc import pull_data


FEATURE = "évjárat"
TRANSFORM = "lda"

X, Y = pull_data(feature=FEATURE)


def plot_raw():
    plot(X[:, ::2], Y, ["DH1", "D13C"], 1)


def plot_pca():
    lX = transform(X, 2, False, "pca")
    plot(lX, Y, ["PC1", "PC2"], 1)


def plot_lda():
    lX = transform(X, 2, False, "lda", y=Y)
    plot(lX, Y, ["LF1", "LF2"], 1)


def plot_ica():
    lX = transform(X, 2, False, "ica")
    plot(lX, Y, ["IC1", "IC2"], 1)


# def plot_ae():
#     lX = transform(X, 2, False, "ae", y=Y)
#     plot(lX, Y, ["F01", "F02"], 1)


if __name__ == '__main__':
    for f in [func for name, func in globals().items() if name[:5] == "plot_"]:
        f()
