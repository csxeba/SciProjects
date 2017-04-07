from matplotlib import pyplot as plt
from matplotlib import mlab

from csxdata import CData
from csxdata.stats import inspection

frame = CData("/home/csa/SciProjects/Project_zsindely/zsindsum.csv",
              indeps=5, headers=1, cross_val=0,
              dehungarize=True, decimal=True,
              feature="PHASE")

axlab = ("DH1", "D13C")
axlab_latex = (r"$(D/H)_I$", r"$\delta^{13}C$")


def do_inspection():
    from csxdata.stats import normality
    inspection.correlation(frame.learning, names=frame._header[-2:])
    normality.full(frame)


def normality_boxwhisker(X, paramname):
    plt.boxplot(X)
    plt.title(paramname)
    plt.show()


def normality_histogram(X, paramname):
    n, bins, patches = plt.hist(X, 10, alpha=0.75, normed=1,
                                facecolor="green",
                                edgecolor="black")
    mu, sigma = X.mean(), X.std()
    y = mlab.normpdf(bins, mu, sigma)
    plt.plot(bins, y, "r--", linewidth=1)
    plt.title(paramname + " hisztogram")
    plt.xlabel(paramname)
    plt.ylabel("Valószínűség")
    plt.show()
