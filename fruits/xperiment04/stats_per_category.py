import pandas as pd

from SciProjects.fruits import projectroot


def print_summaries(cat):
    for c in cat:
        x = X[X["FAMILIA"] == c]  # type: pd.DataFrame
        print()
        print("-"*50)
        print(c)
        desc = x.describe()
        print(desc.replace(".", ","))


def print_correlations(cat):
    for c in cat:
        x = X[X["FAMILIA"] == c]  # type: pd.DataFrame
        x.corr()
        print()
        print("-"*50)
        print(c, "Pearson's correlation")
        print(x.corr("pearson"))
        print()
        print(c, "Spearman's correlation")
        print(x.corr("spearman"))


if __name__ == '__main__':
    df = pd.read_excel(projectroot + "convert.xlsx")

    X = df.iloc[:, 7:19]
    X["FAMILIA"] = df["FAMILIA"]

    cat = X["FAMILIA"].unique()

    print("GROUP;" + ";".join(X.columns[:-1]))
    for c in cat:
        print(c, ";".join(X[X["FAMILIA"] == c].max(axis=0).astype(str)))
    print("ALL;" + ";".join(X.max(axis=0).astype(str)))
