from matplotlib.mlab import normpdf

from csxdata import CData

from SciProjects.generic import paths

FEATURE = "evjarat"
WHERE = None
EQUALS = None

grapes = CData(*paths["grapes"], cross_val=0, lower=True,
               feature=FEATURE, filterby=WHERE, selection=EQUALS)
X, Y = (grapes.learning, grapes.lindeps)
names = ["DH1", "DH2", "D13C"]


def category_frequencies():
    from csxdata.stats.inspection import category_frequencies
    category_frequencies(Y)


def normality_tests(hist=True):
    from csxdata.stats.normality import full
    full(X)
    if hist:
        from matplotlib import pyplot as plt
        f, axes = plt.subplots(1, 3)
        for i, (ax, name) in enumerate(zip(axes, names)):
            ax.set_title(name)
            feature = X[:, i]
            mean, std = feature.mean(), feature.std()
            n, bins, patches = ax.hist(feature, 10, normed=1, facecolor="green", alpha=0.75)
            y = normpdf(bins, mean, std)
            axes[i].plot(bins, y, "r--", linewidth=1)
            ax.grid(True)
        plt.show()


def correlations():
    from csxdata.stats.inspection import correlation
    correlation(X, names)

if __name__ == '__main__':
    category_frequencies()
