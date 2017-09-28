import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from sklearn.feature_selection import f_classif

from csxdata.utilities.parser import parse_csv
from csxdata.utilities.vectorop import split_by_categories
from csxdata.utilities.highlevel import transform
from csxdata.visual import Plotter2D

from SciProjects.sophie import axtitles

currentroot = "/home/csa/SciProjects/Project_Sophie/"

orange = ["orange", 103.378571428571, -25.8928571428571,
          6.53412087912087, 2.09763736263736, -0.635989010989013]

colors = {
    "alma": "green",
    "cser": "red",
    "cuko": "black",
    "kuko": "black",
    "megg": "red",
    "kajs": "yellow",
    "szil": "purple"
}


def get_ellipse_data(line):
    name = line[0]
    vec = np.array(line[1:]).astype(float)
    cov = np.zeros((2, 2))
    cov[0, 0] += vec[2]
    cov[1, 1] += vec[3]
    cov[0, 1] = cov[1, 0] = vec[4]
    means = vec[:2]
    return means, cov, name


def add_reference_ellipses(ax, sigma, these=None):
    data = open(currentroot + "RefEllipses.csv").read().split("\n")
    data = [line.split("\t") for line in data[1:] if line]
    for line in data:
        means, cov, name = get_ellipse_data(line)
        if these is not None:
            if name not in these:
                continue
        add_ellipse(ax, means, cov, sigma, colors[name[:4]], name+" referencia átlag")


def add_ellipse(ax, means, cov, sigma, color, name, **kw):
    from matplotlib.patches import Ellipse
    vals, vecs = np.linalg.eig(cov)

    w = np.sqrt(vals[0]) * sigma * 2
    h = np.sqrt(vals[1]) * sigma * 2
    theta = np.degrees(np.arctan2(*vecs[:, 0][::-1]))

    ell = Ellipse(xy=means, width=w, height=h, angle=theta, **kw)
    ell.set_facecolor("none")
    ell.set_edgecolor(color)
    ax.scatter(means[0], means[1], color=color, marker="x")
    ax.add_patch(ell)
    ax.annotate(name, xy=means, xycoords="data",
                horizontalalignment="right",
                verticalalignment="bottom")


def load_eu_irms():
    X, Y, head = parse_csv(currentroot + "EUborIRMS.csv", decimal=True)
    return X[:, 0], X[:, 1].ravel(), Y.ravel()


def load_eu_nmr():
    X, Y, head = parse_csv(currentroot + "EUborNMR.csv", decimal=True)
    return X[:, 0], X[:, 1].ravel(), Y.ravel()


def load_world_nmr():
    X, Y, head = parse_csv(currentroot + "WW_NMR.csv", decimal=True)
    return X[:, 0], X[:, 1].ravel(), Y.ravel()


def load_eu_full():
    X, Y, head = parse_csv(currentroot + "EUborMinden.csv", decimal=True)
    return X, Y.ravel()


def load_italian_data():
    return np.array(
        [[float(d.replace(",", ".")) for d in line.split("\t") if d]
         for line in open(currentroot + "ITAborMinden.csv")
         .read().split("\n")[1:] if line]
    )


def xperiment_param_vs_Ycoord(pnm, param, Y_C, labels, ttl):
    fig = plt.gcf()
    r, p = stats.pearsonr(param, Y_C)
    plotter = Plotter2D(fig, np.stack((Y_C, param), axis=1), labels,
                        axlabels=("Egyenlítőtől való távolság (°)", axtitles[pnm]))
    plotter.split_scatter(sigma=0, dumppath=currentroot + "PIX/")
    plotter.add_trendline(color="red", linewidth=2)
    plotter.add_legend(plt, "lower left", ncol=3)
    plt.title(ttl + "\nPearson korreláció: r = {:.3f}, p = {:.3f}, {}szignifikáns"
              .format(r, p, ("nem" if p > 0.05 else "")))
    plt.show()


def xperiment_ellipses(param, labels, ttl):
    fig = plt.gcf()
    tparam = transform(param, 1, get_model=False, method="lda", y=labels)
    (F,), (p,) = f_classif(tparam, labels)
    plotter = Plotter2D(fig, param, labels, axlabels=[axtitles["DHI"], axtitles["D13C"]])
    # plotter.split_scatter(sigma=0, alpha=.3)
    # plotter.reset_color()
    plotter.split_scatter(center=True)
    add_ellipse(plotter.ax, [92.38, -27.47], np.array([[1.13, 0.32], [0.32, 0.4]]),
                sigma=2, color="magenta", name="beet")
    add_ellipse(plotter.ax, [110.13, -12.17], np.array([[2.09, 0.023], [0.023, 0.46]]),
                sigma=2, color="magenta", name="cane")
    plt.title(ttl + "\nLDA + ANOVA F-teszt: F = {:.3f}, p = {:.3f}, {}szignifikáns"
              .format(F, p, ("nem " if p > 0.05 else "")))
    plt.show()


def xperiment_world_correlation(pnm, param, Y_C, labels, ttl):
    fig = plt.gcf()
    r, p = stats.pearsonr(param, Y_C)
    plotter = Plotter2D(fig, np.stack((param, Y_C), axis=1), labels,
                        axlabels=["Egyenlítőtől való távolság (°)", axtitles[pnm]])
    plotter.split_scatter(center=True, sigma=0)
    plotter.add_trendline()
    plt.title(ttl + "\nPearson korreláció: r = {:.3f}, p = {:.3f}, {}szignifikáns"
              .format(r, p, ("nem" if p > 0.05 else "")))
    plt.show()


def xperiment_italian(pnm, param, Y_C, ttl):
    line = np.poly1d(np.polyfit(Y_C, param, 1))
    Y_hat = line(Y_C)
    r, p = stats.pearsonr(Y_C, param)
    plt.scatter(Y_C, param, c="black", marker=".")
    plt.plot(Y_C, Y_hat, c="red")
    plt.title(ttl + "\nPearson korreláció: r = {:.3f}; p = {:.3f} {}szignifikáns"
              .format(r, p, "nem " if p > 0.05 else ""))
    ax = plt.gca()
    ax.set_xlabel("Egyenlítőtől való távolság (°)")
    ax.set_ylabel(axtitles[pnm])
    ax.grid(True)
    plt.show()


def xperiment_czhech_samples():

    def plotone(czparam, huparam, pnm):
        plt.title(ttl.format(axtitles[pnm]))
        ax = plt.gca()  # type: plt.Axes

        for i, name in enumerate(sorted(cznmr), start=1):
            czmin, czmax = czparam[name]
            czh = czmax - czmin
            czr = Rectangle((i-0.2, czmin), 0.2, czh, facecolor="red", edgecolor="black")
            ax.add_patch(czr)
            ax.annotate(f"{czmin:.2f}", xy=(i, czmax), xycoords="data",
                        verticalalignment="bottom", horizontalalignment="right")
            ax.annotate(f"{czmax:.2f}", xy=(i, czmin-0.05), xycoords="data",
                        verticalalignment="top", horizontalalignment="right")

            humin, humax = huparam[name]
            huh = humax - humin
            hur = Rectangle((i, humin), 0.2, huh, facecolor="green", edgecolor="black")
            ax.add_patch(hur)
            ax.annotate(f"{humin:.2f}", xy=(i, humax), xycoords="data",
                        verticalalignment="bottom", horizontalalignment="left")
            ax.annotate(f"{humax:.2f}", xy=(i, humin-0.02), xycoords="data",
                        verticalalignment="top", horizontalalignment="left")
            ax.autoscale()

        ax.set_ylabel(axtitles[pnm])
        ax.set_xlim([0, 7])
        ax.set_xticklabels([""] + sorted(cznmr))

        fm = plt.get_current_fig_manager()
        fm.window.showMaximized()

        plt.tight_layout()
        plt.show()

    X, Y, head = parse_csv(currentroot + "cseh.csv", decimal=True)
    cznmr = dict(zip(Y.ravel(), X[:, :2]))
    czirms = dict(zip(Y.ravel(), X[:, 2:]))
    X, Y, head = parse_csv(currentroot + "SZIdata.csv", 4)
    Y = Y[:, 3]
    hudict = split_by_categories(Y.ravel(), X)
    hunmr = {name: (d[:, 0].min(), d[:, 0].max()) for name, d in hudict.items()}
    huirms = {name: (d[:, 2].min(), d[:, 2].max()) for name, d in hudict.items()}
    ttl = "Cseh (piros) és magyar (zöld) {} érték tartományainak összevetése"
    plotone(cznmr, hunmr, "DHI")
    plotone(czirms, huirms, "D13C")


def xperiment_orange():
    ax = plt.gca()
    add_reference_ellipses(ax, 2)
    means, cov, name = get_ellipse_data(orange)
    add_ellipse(ax, means, cov, 2, color="orange", name="narancs", linewidth=3)
    ax.set_xlabel(axtitles["DHI"])
    ax.set_ylabel(axtitles["D13C"])
    plt.grid(True)
    plt.title("Referencia gyümölcs körök és a narancs kör kiemelve")
    plt.show()


def xperiment_sophiexp():
    X, Y, head = parse_csv(currentroot + "SophieXP.csv")
    plotter = Plotter2D(plt.gcf(), X, Y.ravel(),
                        axlabels=[axtitles["DHI"], axtitles["D13C"]])
    add_reference_ellipses(plotter.ax, 2, ["alma"])
    # add_reference_ellipses(plotter.ax, 3, ["alma"])
    plotter.scatter(label_points=plotter.Y)
    plt.show()


def main():

    # ttl = r"$(D/H)_I$ és az egyenlítőtől való távolság közötti összefüggés"
    # param, Y_C, labels = load_eu_nmr()
    # xperiment_param_vs_Ycoord("DHI", param, Y_C, labels, ttl)
    #
    # ttl = r"$\delta^{13}C$ és az egyenlítőtől való távolság közötti összefüggés"
    # param, Y_C, labels = load_eu_irms()
    # xperiment_param_vs_Ycoord("D13C", param, Y_C, labels, ttl)
    #
    # ttl = "Különböző országok $2\sigma$ konfidencia-ellipszisei " + \
    #       "a ${(D/H)_I; \delta^{13}C}$ paramétertérben"
    # param, labels = load_eu_full()
    # xperiment_ellipses(param, labels, ttl)
    #
    # ttl = r"$(D/H)_I$ és az egyenlítőtől való távolság közötti összefüggés világszerte"
    # param, Y_C, labels = load_world_nmr()
    # xperiment_world_correlation("DHI", param, Y_C, labels, ttl)
    #
    # DHI, D13C, Y_C = load_italian_data().T
    #
    # ttl = r"$(D/H)_I$ és az egyenlítőtől való távolság közötti összefüggés az olasz pontoknál"
    # xperiment_italian("DHI", DHI, Y_C, ttl)
    # ttl = r"$\delta^{13}C$ és az egyenlítőtől való távolság közötti összefüggés az olasz pontoknál"
    # xperiment_italian("D13C", D13C, Y_C, ttl)

    xperiment_czhech_samples()

    # xperiment_orange()

    # xperiment_sophiexp()

    pass


if __name__ == '__main__':
    main()
