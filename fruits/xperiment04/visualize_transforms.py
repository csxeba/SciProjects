from csxdata.visual.scatter import Scatter2D
from csxdata.stats import manova

from sklearn.decomposition import PCA, KernelPCA, FastICA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.manifold import SpectralEmbedding

from SciProjects.fruits.fruitframe import FruitData


def transform(X, trname, y=None):
    model = {"pca": PCA(whiten=True), "ica": FastICA(whiten=True),
             "rbf pca": KernelPCA(kernel="rbf"), "lda": LDA(),
             "poly pca": KernelPCA(kernel="poly", degree=2),
             "se": SpectralEmbedding(n_components=3, n_jobs=4)
             }[trname.lower()]
    return model.fit_transform(X, y)[:, :2]


def plot_transform(trname, feature):
    df = FruitData(transform=True)
    X, Y = df.isotope, df[feature]
    lX = transform(X, trname, Y)
    F, p = manova(X.as_matrix(), Y.as_matrix())
    scat = Scatter2D(lX, Y.as_matrix(), axlabels=[f"LatentFactor{i}" for i in range(1, 3)],
                     title=f"Transformation: {feature.upper()}\nF = {F:.4f}; p = {p:.4f}")
    # scat.scatter()
    scat.split_scatter(show=True)


if __name__ == "__main__":
    plot_transform("lda", "EV")
