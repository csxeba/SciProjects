import pandas as pd

from SciProjects.rich import projectroot


def pull_data(rescale=True):
    df = pd.read_excel(projectroot + "Filled.xlsx")

    stocks = df.as_matrix().astype(float)
    if rescale:
        stocks /= stocks.max(axis=0)
        stocks -= stocks.mean(axis=0, keepdims=True)
    return stocks, df.columns
