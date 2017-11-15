from csxdata.visual.scatter import Scatter3D

from sklearn.decomposition import PCA, KernelPCA, FastICA, FactorAnalysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

from SciProjects.fruits.fruitframe import FruitData


def transform(X, trname, y=None):
    model = {"pca": PCA(whiten=True), "ica": FastICA(whiten=True),
             "kpca": KernelPCA(kernel="rbf"), "lda": LDA(), "fa": FactorAnalysis()
             }[trname.lower()]
    return model.fit_transform(X, y)[:, :3]


def plot_transform(trname, feature):
    df = FruitData(transform=True)
    X, Y = df.volatile, df[feature]
    lX = transform(X, trname, Y)
    scat = Scatter3D(lX, Y.as_matrix(), axlabels=[f"LatentFactor{i}" for i in range(1, 4)],
                     title=f"Transformation: {feature.upper()}")
    # scat.scatter()
    scat.split_scatter()


if __name__ == "__main__":
    plot_transform("fa", "FAMILIA")
