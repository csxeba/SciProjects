import numpy as np
import pandas as pd

from SciProjects.riskanalyze import projectroot


class Failer:

    @staticmethod
    def bdensity15(df, useR=True):
        minimum = 820. - (0.5 if useR else 0.)
        maximum = 845. + (0.5 if useR else 0.)
        return np.logical_or(df["SŰR"] < minimum, df["SŰR"] > maximum)

    @staticmethod
    def bviscosity40(df, useR=True):
        minimum = 2.
        maximum = 4.5
        if useR:
            minimum -= 0.0082 * minimum * (minimum+1)
            maximum += 0.0082 * maximum * (maximum+1)
        return np.logical_or(df["VISZK"] < minimum, df["VISZK"] > maximum)

    @staticmethod
    def bdistillation250(df, useR=True):
        maximum = 65. + (2.7 if useR else 0.)
        return df["D250"] > maximum

    @staticmethod
    def bdistillation350(df, useR=True):
        minimum = 85. - (2.7 if useR else 0.)
        return df["D350"] < minimum

    @staticmethod
    def bdistillation95perc(df, useR=True):
        maximum = 360.
        if useR:
            maximum += 0.04227 * (360. - 140.)
        return df["95D"] > maximum

    @staticmethod
    def bFAME(df, useR=True):
        maximum = 7.
        if useR:
            maximum += 0.0793 * 7. + 0.0413
        return df["FAME"] > maximum

    @staticmethod
    def bsulphur(df):
        return df["KÉN"] > 12.

    @staticmethod
    def blobp(df):
        return df["LOBP"] < 53.

    @staticmethod
    def do_all(df):
        for funcname in ("bdensity15", "bviscosity40", "bdistillation250",
                         "bdistillation350", "bdistillation95perc",
                         "bFAME", "bsulphur", "blobp"):
            df[funcname] = getattr(Failer, funcname)(df)
        return df


dpath = projectroot + "adat/OlajMinden.xlsx"

print("Reading", dpath)
data = pd.read_excel(dpath, header=0)
print(data.dtypes)
fail = Failer.do_all(data)
fail.to_excel(projectroot + "FAILZ.xlsx")
