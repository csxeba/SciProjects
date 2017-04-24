import numpy as np
from scipy import stats

from matplotlib import pyplot as plt

from csxdata.utilities.parsers import parse_csv
from csxdata.utilities.vectorops import split_by_categories, discard_NaN_rows

from SciProjects.sophie import projectroot


def split_by_CCode(param):
    bycat = split_by_categories(param, CCode, argsonly=True)
    new = {}
    for cat in bycat:
        catargs = bycat[cat]
        fX, fCoord = discard_NaN_rows(param[catargs], Y_C[catargs])
        if not np.prod(fX.shape):
            continue
        new[cat] = [fX.mean(), fX.std(), fCoord.mean()]
    return new


def plotem(byCCode, pnm):
    annot = sorted([n for n in byCCode])
    X, std, Y = np.array([byCCode[n] for n in annot]).T
    ax = plt.gca()
    # ax.errorbar(Y, X, yerr=std*2, fmt="bX",
    #             ecolor="red", elinewidth=1,
    #             capsize=4)
    ax.scatter(Y, X, color="blue", marker="X")
    fit = np.polyfit(Y, X, 1)
    lin = np.poly1d(fit)
    ax.plot(Y, lin(Y), "r-")
    r, p = stats.pearsonr(X, lin(Y))
    for label, y, x in zip(annot, Y, X):
        ax.annotate(label, xy=(y, x), xycoords="data",
                    horizontalalignment="right",
                    verticalalignment="top")
    ax.set_xlabel("Y koordináta")
    ax.set_ylabel(pnm)
    plt.title("Országos {} átlagértékek\n$r^2 = {:.2f}$, $p = {:.2f}$, {}szignifikáns"
              .format(pnm, r**2, p, "nem " if p > 0.05 else ""))
    plt.show()


data, labels, header = parse_csv(projectroot + "01GEO.csv", indeps=2, headers=1,
                                 dehungarize=True, decimal=True, sep="\t")
X_C, Y_C, DHI, D13C = data.T


CCode = labels[:, 0]

dh1cc = split_by_CCode(DHI)
d13cc = split_by_CCode(D13C)
plotem(dh1cc, "$(D/H)_I$")
plotem(d13cc, "r$\delta^{13}C$")
