import numpy as np
from scipy import stats

from matplotlib import pyplot as plt

from csxdata.utilities.vectorop import split_by_categories, dropna

from SciProjects.sophie import pull_data, axtitles


def split_by_CCode(param):
    bycat = split_by_categories(CCode)
    new = {}
    for cat in bycat:
        catargs = bycat[cat]
        fX, fCoord = dropna(param[catargs], Y_C[catargs])
        if not np.prod(fX.shape):
            continue
        new[cat] = [fX.mean(), fX.std(), fCoord.mean()]
    return new


def correlate(pnm):
    param = globals()[pnm]
    X, Y = dropna(param, Y_C)
    return stats.spearmanr(X, Y)


def plotem(byCCode, pnm, absolute):
    annot = sorted([n for n in byCCode])
    X, std, Y = np.array([byCCode[n] for n in annot]).T
    ax = plt.gca()
    # ax.errorbar(Y, X, yerr=std*2, fmt="bX",
    #             ecolor="red", elinewidth=1,
    #             capsize=4)
    south = np.zeros_like(Y)
    south[Y < 0.] = 1.
    south = south.astype(bool)
    aY = np.abs(Y)
    ax.scatter(Y[south], X[south], color="red", marker="o", s=7)
    ax.scatter(aY[south], X[south], color="red", marker="o", s=7)
    ax.scatter(aY[~south], X[~south], color="black", marker="o", s=7)
    fit1 = np.polyfit(Y[~south], X[~south], 1)
    fit2 = np.polyfit(Y[south], X[south], 1)
    print("FIT1:", fit1)
    print("FIT2:", fit2)
    lin = np.poly1d(fit1)
    _time_scatter(Y, lin(Y), "r-")
    lin = np.poly1d(fit2)
    _time_scatter(Y, lin(Y), "r-")
    r, p = correlate(pnm)
    for label, y, x in zip(annot, Y, X):
        ax.annotate(label, xy=(y, x), xycoords="data",
                    horizontalalignment="right",
                    verticalalignment="top")
    ax.set_xlabel("Egyenlítőtől való távolság")
    ax.set_ylabel(axtitles[pnm])
    ttl = "\n".join((
        "Országos {} átlagértékek",
        "Spearman rang-korreláció: $r = {:.2f}$, $p = {:.2f}$, {}szignifikáns"
    ))
    plt.title(ttl.format(axtitles[pnm], r**2, p, "nem " if p > 0.05 else ""))
    plt.grid(True)
    plt.show()


X_C, Y_C, DHI, D13C, CCode = pull_data("04GEO_full.csv", sep=";")

dh1cc = split_by_CCode(DHI)
d13cc = split_by_CCode(D13C)
plotem(dh1cc, "DHI", absolute=False)
plotem(d13cc, "D13C", absolute=False)
