import pandas as pd

from sklearn.discriminant_analysis import (
    LinearDiscriminantAnalysis as LDA
)

from csxdata.visual.scatter import Scatter3D

from SciProjects.fruits import projectroot


def main():
    df = pd.read_excel(projectroot + "convert.xlsx")
    X, Y = df.loc[:, "ACALD":], df["GYUM"]
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
