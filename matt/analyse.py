import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

from csxdata.visual.scatter import Scatter2D

from SciProjects.matt import projectroot


def plotdata(lX, Y, title):
    plotter = Scatter2D(lX, Y, title=title, axlabels=["F01", "F02"])
    plotter.split_scatter()
    plt.legend()
    plt.show()


df = pd.read_excel(projectroot + "adat.xlsx")

X, Y = df.iloc[:, 1:].as_matrix(), df["GYUM"].as_matrix()

pca = PCA(n_components=2)
lda = LDA(n_components=2)

pcaX = pca.fit_transform(X)
ldaX = lda.fit_transform(X, Y)

pca_title = f"PCA\nTotal explained variance: {pca.explained_variance_ratio_.sum():.2%}"
lda_title = f"LDA\nTotal explained variance: {lda.explained_variance_ratio_.sum():.2%}"

plotdata(pcaX, Y, pca_title)
plotdata(ldaX, Y, lda_title)

# x = X.dropna().as_matrix()
#
# full(x, names=X.columns)
# for colname in X:
#     fullplot(X[colname].dropna().as_matrix(), colname, histbins=7)
#
# stats.correlation(X.dropna().as_matrix(), X.columns)

