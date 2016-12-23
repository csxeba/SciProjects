import numpy as np
from matplotlib.mlab import normpdf

from project_grapes.misc import pull_data, stringeq


FEATURE = "évjárat"
WHERE = None
EQUALS = None

X, Y = pull_data(frame=False, feature=FEATURE, filterby=WHERE, selection=EQUALS)
names = ["DH1", "DH2", "D13C"]


def category_frequencies():
    print("-"*38)
    header = "Category: {}".format(FEATURE)
    if WHERE:
        header += " where {} = {}".format(WHERE, EQUALS)
    print(header)

    categ = list(set(Y))
    nums = []
    rates = []

    for cat in categ:
        eq = stringeq(Y, cat)
        num = np.sum(eq)
        rate = num / Y.shape[0]
        rates.append(rate)
        nums.append(num)

    for cat, num, rate in sorted(zip(categ, nums, rates), key=lambda x: x[1], reverse=True):
        print("{0:<20}    {1:>3}    {2:>7.2%}".format(cat, num, rate))

    print("-"*38)
    print("{0:<20}    {1:>3}    {2:.2%}".format("SUM", Y.shape[0], sum(rates)))


def normality_tests(hist=True):
    from csxdata.stats import full
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
    from scipy.stats import spearmanr
    from matplotlib import pyplot as plt
    pcorr = np.abs(np.corrcoef(X, rowvar=0))
    pprob = np.greater_equal(np.abs(pcorr), 0.113).astype(int)
    scorr, sprob = np.abs(spearmanr(X, axis=0))
    sprob = np.less_equal(sprob, 0.05).astype(int)

    fig, axes = plt.subplots(2, 2)
    mats = [[pcorr, scorr], [pprob, sprob]]
    for rown, vec in enumerate(mats):
        for coln, m in enumerate(vec):
            axes[rown][coln].matshow(m, interpolation="none", vmin=0, vmax=1)
            axes[rown][coln].set_xticklabels([""] + names)
            axes[rown][coln].set_yticklabels([""] + names)

    plt.show()

if __name__ == '__main__':
    category_frequencies()
