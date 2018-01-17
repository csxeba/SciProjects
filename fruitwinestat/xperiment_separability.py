import numpy as np

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

from csxdata.stats import inspection, manova, pairwise_T2
from csxdata.visual import scatter
from csxdata.utilities.vectorop import drop_lowNs

from SciProjects.fruitwinestat.merge_data import pull_merged_data, PARAM, projectroot


FEATURE = "EV"


def xperiment():
    df = pull_merged_data(feature=FEATURE).dropna()
    X, Y = df[PARAM].as_matrix(), df[FEATURE].as_matrix()
    inspection.category_frequencies(Y)
    Y, X = drop_lowNs(10, Y, X)
    inspection.correlation(X, names=PARAM)
    pairwise_T2(X, Y, dumproot=projectroot, xpid=f"PairwiseT2_{FEATURE}.xlsx")
    F, p = manova(X, Y)
    print("-"*50)
    lda = LDA(n_components=2).fit(X, Y)  # type: LDA
    smexvar = lda.explained_variance_ratio_
    scat = scatter.Scatter2D(lda.transform(X), Y, title=f"LDA ({smexvar.sum():.2%})\nMANOVA: F = {F:.4f}, p = {p:.4f}",
                             axlabels=[f"Latent0{i} ({ev:.2%})" for i, ev in enumerate(smexvar, start=1)])
    is_many = len(np.unique(Y)) > 5
    scat.split_scatter(legend=not is_many, show=True, center=is_many, label=is_many)


if __name__ == '__main__':
    xperiment()
