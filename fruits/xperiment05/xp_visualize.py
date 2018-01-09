from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

from SciProjects.fruits.xperiment05.util import pull_data

from csxdata.visual import scatter
from csxdata.utilities.vectorop import drop_lowNs
from csxdata.stats import manova, inspection

FEATURE = "EV"

df = pull_data(FEATURE)
X = df[["DH1", "DH2", "D13C"]].as_matrix()
Y = df[FEATURE].as_matrix()

Y, X = drop_lowNs(15, Y, X)

inspection.category_frequencies(Y)

lX = LDA(n_components=2).fit_transform(X, Y)
title = "LDA\nMANOVA F = {:.4f}, {:.4f}".format(*manova(X, Y))
scat = scatter.Scatter2D(lX, Y, title=title, axlabels=[f"Latent0{i}" for i in range(1, 3)])
scat.split_scatter(show=True)
