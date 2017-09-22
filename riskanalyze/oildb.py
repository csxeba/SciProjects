import numpy as np
import pandas as pd

from SciProjects.riskanalyze import projectroot


def fails_on_density15(df, useR=True):
    minimum = 820. - (0.5 if useR else 0.)
    maximum = 845. + (0.5 if useR else 0.)
    return np.logical_or(df["SŰR"] < minimum, df["SŰR"] > maximum)


def fails_on_viscosity40(df, useR=True):
    minimum = 2.
    maximum = 4.5
    if useR:
        minimum -= 0.0082 * minimum * (minimum+1)
        maximum += 0.0082 * maximum * (maximum+1)
    return np.logical_or(df["VISZK"] < minimum, df["VISZK"] > maximum)


def fails_on_distillation250(df, useR=True):
    maximum = 65. + (2.7 if useR else 0.)
    return df["250C"] > maximum


def fails_on_distillation350(df, useR=True):
    maximum = 85. + (2.7 if useR else 0.)
    return df["350C"] > maximum


def fails_on_distillation95perc(df, useR=True):
    maximum = 360.
    if useR:
        maximum += 0.04227 * (360. - 140.)
    return df["95DESZT"] > maximum


def fails_on_FAME(df, useR=True):
    maximum = 7.
    if useR:
        maximum += 0.0793 * 7. + 0.0413
    return df["FAME"] > maximum


def fails_on_sulphur(df):
    return df["KÉN"] > 12.


def fails_on_lobp(df):
    return df["LOBP"] < 53.


dpath = projectroot + "adat/UseMeOlaj.xlsx"

data = pd.read_excel(dpath, header=0)
data = data[~pd.isnull(data)]

mask = fails_on_density15(data)
for func in (fails_on_distillation95perc, fails_on_distillation250, fails_on_lobp,
             fails_on_distillation350, fails_on_FAME, fails_on_sulphur, fails_on_viscosity40):
    print(f"RUNNING {func.__name__}")
    mask = np.logical_or(mask, func(data))

fail = data[mask]

print(f"FAILED: {len(fail)/len(data):.3%}")
