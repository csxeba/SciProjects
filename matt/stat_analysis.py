import pandas as pd
from scipy import stats
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.feature_selection import f_classif

from csxdata.utilities.vectorop import split_by_categories

from SciProjects.matt import projectroot


def do_anova_sp(X, Y):
    sX = split_by_categories(Y, X)
    return stats.f_oneway(*sX)


def do_anova_sklearn(X, Y):
    Fs, ps = f_classif(X, Y)
    return Fs, ps


def xperiment_lda_anova(dframe):
    X, Y = dframe.iloc[:, 1:], dframe.iloc[:, 0]
    lda = LDA(n_components=1)
    lX = lda.fit_transform(X, Y)

    # spF, spp = do_anova_sp(X, Y)
    skF, skp = do_anova_sklearn(X, Y)
    (ldF,), (ldp,) = do_anova_sklearn(lX, Y)

    print("Explained variance:", lda.explained_variance_ratio_[0])
    print(f"skF: {skF}, skp: {skp}\nldF: {ldF}, ldp: {ldp}")


def xperiment_pairwise_t2(dframe):
    import itertools
    from csxdata.stats import hotelling_T2
    for a, b in itertools.combinations(["Alma", "Kajszi", "Málna"], 2):
        print(f"{a} vs {b}: ", end="")
        catA = dframe[dframe["GYUM"] == a].iloc[:, 1:].as_matrix()
        catB = dframe[dframe["GYUM"] == b].iloc[:, 1:].as_matrix()
        F, p = hotelling_T2(catA, catB)
        print(f"F = {F:.5f}, p = {p}")


if __name__ == '__main__':
    df = pd.read_excel(projectroot + "adat.xlsx", header=0)
    xperiment_pairwise_t2(df)
