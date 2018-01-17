from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

from csxdata.visual import Scatter2D
from csxdata.stats import manova, pairwise_T2
from csxdata.learning import supervised

from SciProjects.fruitwinestat import projectroot
from SciProjects.fruitwinestat.merge_data import pull_merged_data, as_learningtable, PARAM

XPID = "Wine_Fruit_merge"


def xperiment_classification(df, feature):
    featurekw = {"MEGYE": dict(center=True, label=True, legend=False), "EV": dict()}
    X, Y = as_learningtable(df[[feature] + PARAM].dropna(), feature, normalize=True, split=0, dropthresh=10)
    lda = LDA(n_components=2).fit(X, Y)
    lX = lda.transform(X)

    F, p = manova(X, Y)
    pairwise_T2(X, Y, dumproot=projectroot, xpid=XPID)

    title = f"{feature} LDA ({lda.explained_variance_ratio_.sum():.2%})\nMANOVA F = {F:.2f}, p = {p:.4f}"

    Scatter2D(
        lX, Y, title=title, axlabels=[f"Latent0{i}" for i in range(lX.shape[-1])]
    ).split_scatter(show=True, **featurekw[feature])


def xperiment_supervised(df):
    learning_suite = supervised.SupervisedSuite(exclude_models="mlp")
    learning_suite.run_experiments(df, labels=["MEGYE", "EV"], features=PARAM,
                                   outxlsx=f"{projectroot}{XPID}_supervised.xlsx")


def main():
    df = pull_merged_data()
    xperiment_supervised(df)


if __name__ == '__main__':
    main()
