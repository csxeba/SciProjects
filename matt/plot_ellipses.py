import pandas as pd

from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

from csxdata.visual.scatter import Scatter2D

from SciProjects.matt import projectroot


def plotit(X, Y, modeltype):
    model = globals()[modeltype](n_components=2)
    tX = model.fit_transform(X, y=Y)
    exvr = model.explained_variance_ratio_
    scat = Scatter2D(tX, Y, title=modeltype, axlabels=[
        f"Factor 1 ({exvr[0]:.2%})", f"Factor 2 ({exvr[1]:.2%})"
    ])
    scat.split_scatter()
    scat.add_legend(plt)
    plt.show()


df = pd.read_excel(projectroot + "Param_szurt.xlsx")

plotit(df.loc[:, "D13C":"log_3M1B"].as_matrix(), df.loc[:, "GYUM"].as_matrix(), "PCA")
plotit(df.loc[:, "D13C":"log_3M1B"].as_matrix(), df.loc[:, "GYUM"].as_matrix(), "LDA")
