from sklearn.decomposition import PCA, FastICA, KernelPCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.manifold import SpectralEmbedding

from csxdata.stats import manova
from csxdata.stats.inspection import category_frequencies
from csxdata.visual.scatter import Scatter2D, Scatter3D
from csxdata.utilities.vectorop import standardize

from SciProjects.vinyard.utility import read_datasets


def get_transformator(ndim, transformation):
    return {
        "pca": PCA(n_components=ndim, whiten=True),
        "ica": FastICA(n_components=ndim),
        "lda": LDA(n_components=ndim),
        "rbf-pca": KernelPCA(n_components=ndim, kernel="rbf"),
        "poly-pca": KernelPCA(n_components=ndim, kernel="poly", degree=2),
        "se": SpectralEmbedding(n_components=ndim)
    }[transformation.lower()]


def xperiment(transform, ndim):
    X, Y = read_datasets(ycol="YEAR", dropthresh=10)
    category_frequencies(Y)
    F, p = manova(X, Y)
    X = standardize(X)
    model = get_transformator(ndim, transform)
    lX = model.fit_transform(X, Y)

    expvar = model.explained_variance_ratio_[:ndim]
    plottitle = f"{transform.upper()} ({sum(expvar):.2%})\nMANOVA F = {F:.4f}, p = {p:.4f}"
    axlabels = [f"Latent0{i+1} ({expvar[i]:.2%})" for i in range(ndim)]

    if ndim == 2:
        scat = Scatter2D(lX, Y, title=plottitle, axlabels=axlabels)
    elif ndim == 3:
        scat = Scatter3D(lX, Y, title=plottitle, axlabels=axlabels)
    else:
        raise ValueError(f"Unsupported dimensionality: {ndim}")

    scat.split_scatter(legend=True, show=True)


if __name__ == "__main__":
    xperiment("lda", 2)
