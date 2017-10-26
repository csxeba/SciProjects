import pandas as pd
from matplotlib import pyplot as plt

from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

from csxdata.visual.scatter import Scatter2D

from SciProjects.isovol import projectroot


def plotdata(lX, Y, title, method):
    plotter = Scatter2D(lX, Y, title=title, axlabels=["F01", "F02"])
    plotter.split_scatter()
    plt.legend()
    # plt.savefig(f"{projectroot}N27.Results/{method}_plot.png")
    plt.show()


def transformplot():
    pca = PCA(n_components=2)
    lda = LDA(n_components=3)
    pcaX = pca.fit_transform(X)
    ldaX = lda.fit_transform(X, Y)
    # pd.DataFrame(lda.coef_).to_excel(projectroot + "LDA_components.xlsx")
    print(lda.explained_variance_ratio_)
    pca_title = f"PCA\nTotal explained variance: {pca.explained_variance_ratio_.sum():.2%}"
    lda_title = f"LDA\nTotal explained variance: {lda.explained_variance_ratio_.sum():.2%}"
    plotdata(pcaX, Y, pca_title, "PCA")
    plotdata(ldaX, Y, lda_title, "LDA")


df = pd.read_excel(projectroot + "AllData.zrg.xlsx")
print(df.dtypes)

X, Y = df.loc[:, "iMETOH":"iAMYL"].as_matrix(), df["GYUM"].as_matrix()
transformplot()
