from csxdata.visual.scatter import Scatter2D, Scatter3D
from csxdata.stats import manova

from sklearn.decomposition import PCA, KernelPCA, FastICA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.manifold import SpectralEmbedding

from SciProjects.fruits.fruitframe import FruitData


def transform(X, trname, ndim, y=None):
    return {"pca": PCA(whiten=True, n_components=ndim),
            "ica": FastICA(whiten=True, n_components=ndim),
            "lda": LDA(n_components=ndim),
            "rbf pca": KernelPCA(kernel="rbf", n_components=ndim),
            "poly pca": KernelPCA(kernel="poly", degree=2, n_components=ndim),
            "se": SpectralEmbedding(n_components=ndim, n_jobs=4)
    }[trname.lower()].fit_transform(X=X, y=y)


def plot_transform(trname, feature, ndim):
    df = FruitData(transform=True)
    X, Y = df.X, df[feature]
    lX = transform(X, trname, ndim, Y)
    F, p = manova(X.as_matrix(), Y.as_matrix())
    if ndim == 2:
        scat = Scatter2D(lX, Y.as_matrix(), axlabels=[f"LatentFactor{i}" for i in range(1, 3)],
                         title=f"Transformation: {feature.upper()}\nF = {F:.4f}; p = {p:.4f}")
    elif ndim == 3:
        scat = Scatter3D(lX, Y.as_matrix(), axlabels=[f"LatentFactor{i}" for i in range(1, 4)],
                         title=f"Transformation: {feature.upper()}\nF = {F:.4f}; p = {p:.4f}")
    else:
        raise ValueError(f"Invalid ndim: {ndim}")
    # scat.scatter()
    scat.split_scatter(show=True)


if __name__ == "__main__":
    plot_transform("poly pca", "FAMILIA", 2)
