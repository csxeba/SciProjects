import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

from csxdata.visual.scatter import Scatter2D
from csxdata.visual.histogram import fullplot
from csxdata.stats.normaltest import full
from csxdata.stats.inspection import correlation

from SciProjects.matt import projectroot


def plotdata(lX, Y, title, method):
    plotter = Scatter2D(lX, Y, title=title, axlabels=["F01", "F02"])
    plotter.split_scatter()
    plt.legend()
    plt.savefig(f"{projectroot}N27.Results/{method}_plot.png")
    plt.show()


def transformplot():
    pca = PCA(n_components=2)
    lda = LDA(n_components=2)
    pcaX = pca.fit_transform(X)
    ldaX = lda.fit_transform(X, Y)
    pca_title = f"PCA\nTotal explained variance: {pca.explained_variance_ratio_.sum():.2%}"
    lda_title = f"LDA\nTotal explained variance: {lda.explained_variance_ratio_.sum():.2%}"
    plotdata(pcaX, Y, pca_title, "PCA")
    plotdata(ldaX, Y, lda_title, "LDA")


def normality():
    paramnames = df.columns[1:]
    full(X, names=paramnames)
    for i, colname in enumerate(paramnames):
        outpath = f"{projectroot}N27.Results/{colname}.png"
        fullplot(X[:, i], colname, histbins=7, show=False, dumppath=outpath)
    correlation(X, paramnames)


if __name__ == '__main__':
    df = pd.read_excel(projectroot + "adat.xlsx", header=0)
    X, Y = df.iloc[:, 1:].as_matrix(), df["GYUM"].as_matrix()
    transformplot()
