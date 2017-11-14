from sklearn.discriminant_analysis import (
    LinearDiscriminantAnalysis as LDA
)

from csxdata.visual.scatter import Scatter3D

from SciProjects.fruits.fruitframe import FruitData


def main():
    df = FruitData(transform=True)
    X, Y = df.volatile, df["FAMILIA"]
    lda = LDA(n_components=3).fit(X, Y)
    print("Expained variances:", lda.explained_variance_ratio_)
    lX = lda.transform(X)
    scat = Scatter3D(lX, Y.as_matrix(), axlabels=[
        f"DF0{i} ({var:.2%})" for i, var in enumerate(lda.explained_variance_ratio_, start=1)
    ])
    # scat.scatter()
    scat.split_scatter()


if __name__ == "__main__":
    main()
