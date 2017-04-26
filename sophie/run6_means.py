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


def correlate(pnm):
    param = globals()[pnm]
    X, Y = discard_NaN_rows(param, Y_C)
    return stats.spearmanr(X, Y)


def plotem(byCCode, pnm, absolute):
    annot = sorted([n for n in byCCode])
    X, std, Y = np.array([byCCode[n] for n in annot]).T
    ax = plt.gca()
    # ax.errorbar(Y, X, yerr=std*2, fmt="bX",
    #             ecolor="red", elinewidth=1,
    #             capsize=4)
    if absolute:
        Y = np.abs(Y)
    ax.scatter(Y, X, color="black", marker="o", s=7)
    fit = np.polyfit(Y, X, 1)
    lin = np.poly1d(fit)
    ax.plot(Y, lin(Y), "r-")
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


axtitles = {"DHI": "$(D/H)_I$ (ppm)", "D13C": "$\\delta^{13}C$ (‰)"}

data, labels, header = parse_csv(projectroot + "01GEO.csv", indeps=2, headers=1,
                                 dehungarize=True, decimal=True, sep="\t")
X_C, Y_C, DHI, D13C = data.T


CCode = labels[:, 0]

dh1cc = split_by_CCode(DHI)
d13cc = split_by_CCode(D13C)
plotem(dh1cc, "DHI", absolute=True)
plotem(d13cc, "D13C", absolute=False)
