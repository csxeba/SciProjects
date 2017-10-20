import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

from csxdata.visual.scatter import Scatter2D
from csxdata.visual.histogram import fullplot
from csxdata.stats.normaltest import full
from csxdata.stats.inspection import correlation

from SciProjects.matt import projectroot


def plotdata(lX, Y, title):
    plotter = Scatter2D(lX, Y, title=title, axlabels=["F01", "F02"])
    plotter.split_scatter()
    plt.legend()
    plt.show()


def pca_scree():
    pca = PCA()
    pca.fit(X)
    aran = np.arange(1, pca.n_components_ + 1)
    plt.plot(aran, pca.explained_variance_ratio_, "b-")
    plt.scatter(aran, pca.explained_variance_ratio_)
    plt.title("PCA explained variance ratios")
    plt.xticks(aran)
    plt.grid(True)
    plt.xlabel("Number of Eigenvalue")
    plt.ylabel("Eigenvalue")
    ax = plt.gca()
    ax.set_yticklabels([f"{tick*pca.explained_variance_.sum():.2f}" for tick in ax.get_yticks()])
    cs = 0
    for x, y in enumerate(pca.explained_variance_ratio_, start=1):
        cs += y
        plt.annotate(f"{cs:.2%}", xy=(x, y))
    plt.show()


def transformplot():
    pca = PCA()
    lda = LDA()
    pcaX = pca.fit_transform(X)
    ldaX = lda.fit_transform(X, Y)
    pca_title = f"PCA\nTotal explained variance: {pca.explained_variance_ratio_[:2].sum():.2%}"
    lda_title = f"LDA\nTotal explained variance: {lda.explained_variance_ratio_[:2].sum():.2%}"
    plotdata(pcaX[:, :2], Y, pca_title)
    plotdata(ldaX[:, :2], Y, lda_title)


def normality():
    paramnames = df.columns[1:]
    full(X, names=paramnames)
    for i, colname in enumerate(paramnames):
        fullplot(X[:, i], colname, histbins=7)
    correlation(X, paramnames)


if __name__ == '__main__':
    df = pd.read_excel(projectroot + "adat.xlsx", header=0)
    print(df.kurt())
    # print(df.dtypes)
    # X, Y = df.iloc[:, 1:].as_matrix(), df["GYUM"].as_matrix()
    # normality()
