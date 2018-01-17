import pandas as pd

from csxdata.utilities.vectorop import split_dataset, drop_lowNs

from SciProjects.fruitwinestat import projectroot
from SciProjects.vinyard.utility import WineData
from SciProjects.fruits.fruitframe import FruitData


PARAM = ["DH1", "DH2", "D13C"]


def pull_merged_data(feature=None, drop_outliers=True, force_reread=False, report=False) -> pd.DataFrame:
    if force_reread:
        wd = WineData()
        wdf = wd.raw[["COUNTY", "YEAR"] + PARAM]  # type: pd.DataFrame
        wdf.rename(columns={"COUNTY": "MEGYE", "YEAR": "EV"}, inplace=True)
        fd = FruitData()
        fdf = fd.raw[["MEGYE", "EV"] + PARAM]

        df = pd.concat((wdf, fdf))  # type: pd.DataFrame
        df.to_excel(projectroot + "Merged.xlsx")
    else:
        df = pd.read_excel(projectroot + "Merged.xlsx")
    if report:
        print(df.columns)
        print()
        print(df.describe())
        print()
        print(df.dtypes)
    if drop_outliers:
        # mask = np.logical_or(, df["DH1"] > 90)
        df = df[df["DH2"] < 135]
        df = df[df["DH1"] > 90]
    return df[[feature] + PARAM].dropna() if feature else df


def as_learningtable(df, feature, normalize=True, split=0.1, dropthresh=10):
    X, Y = df[PARAM].as_matrix(), df[feature].as_matrix()
    Y, X = drop_lowNs(dropthresh, Y, X)
    output = split_dataset(X, Y, split, shuff=True, normalize=normalize) if split else (X, Y)
    return output


if __name__ == '__main__':
    pull_merged_data(feature=None, force_reread=True)
