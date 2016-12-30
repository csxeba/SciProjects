import warnings

import numpy as np

from csxdata import roots
from csxdata.utilities.parsers import parse_csv


def pull_data(absval=False, param=0, transformation=None, label="familia",
              paramset="all"):
    if transformation and len(transformation) > 4:
        transformation = transformation[:4]
    elif not transformation:
        transformation = "raw"

    inflpath = roots["csvs"] + "kozma.csv"

    data, Ys, head = parse_csv(path=inflpath, indeps=3, headers=1,
                               sep="\t", end="\n", dtype=float)

    prm = paramset.lower()[:3]
    if prm == "iso":
        independent = data[:, :3]
    elif prm == "fus":
        independent = data[:, 3:]
    else:
        independent = data

    if label[:3].lower() == "fam":
        dependent = Ys[:, 1]  # Familia
    elif label[:3].lower() == "spe":
        dependent = Ys[:, 2]  # Species
    else:
        raise RuntimeError("Specified labelling does not exist")

    dependent = np.array([label[:5] for label in dependent])

    if absval:
        independent = np.abs(independent)

    if transformation in ("pca", "lda", "ica", "ae", "pls"):
        if not param:
            warnings.warn("No params supplied for matrix transform. Assuming maximum.")
            param = None
        independent = matrix_transformation(independent, dependent, param, transformation)
    elif transformation in ("sigm", "log", "sqrt", "sinu", "fft"):
        if param:
            warnings.warn("Params supplied for parameter transformation. Ignoring!")
        independent = independent[:, (0, 2)]
        independent[:, 0] = parameter_transformation(independent[:, 0], transformation)
    elif transformation == "raw":
        pass
    else:
        raise RuntimeError("Specified transformation not understood or wrong param supplied!")

    return independent, dependent


def pull_validation_data(label="familia", paramset="all"):
    X, y, head = parse_csv(roots["csv"] + "gyumzsind.csv", indeps=3, headers=1)
    if label.lower()[:3] == "fam":
        y = y[:, 1]
    elif label.lower()[:3] == "spe":
        y = y[:, 2]
    y = np.array([y[:5] for y in y])

    prm = paramset.lower()[:3]
    if prm == "iso":
        X = X[:, :3]
    elif prm == "fus":
        X = X[:, 3:]
    elif prm == "all":
        pass
    else:
        raise RuntimeError("No such parameter set!")

    return X, y


def pull_fruits_data(transformation=None, param=0):
    if transformation and len(transformation) > 4:
        transformation = transformation[:4]
    elif not transformation:
        transformation = "raw"

    inflpath = roots["csvs"] + "grapes.csv"

    data, Ys, head = parse_csv(path=inflpath, indeps=5, headers=1)

    independent = data[:, -3:]

    dependent = Ys[:, 3]  # Borvidek
    dependent = np.array([label[:5] for label in dependent])

    if transformation in ("pca", "lda", "ica", "ae", "pls"):
        if not param:
            warnings.warn("No params supplied for matrix transform. Assuming maximum.")
            param = None
        independent = matrix_transformation(independent, dependent, param, transformation)
    elif transformation in ("sigm", "log", "sqrt", "sinu", "fft"):
        if param:
            warnings.warn("Params supplied for parameter transformation. Ignoring!")
        independent = independent[:, (0, 2)]
        independent[:, 0] = parameter_transformation(independent[:, 0], transformation)
    elif transformation == "raw":
        pass
    else:
        raise RuntimeError("Specified transformation not understood or wrong param supplied!")

    return independent, dependent


def parameter_transformation(parameter, transformation):
    transformation = transformation[:4].lower()
    if transformation == "sigm":
        mn = np.mean(parameter, axis=0)
        ct = parameter - mn
        parameter = sigmoid(ct)
    elif transformation[:3] == "log":
        parameter = np.log(parameter)
    elif transformation == "sqrt":
        parameter = np.sqrt(parameter)
    elif transformation == "sinu":
        parameter = np.sin(parameter)
    elif transformation == "fft":
        parameter = np.fft.fft(parameter)
    else:
        raise RuntimeError("Specified transformation ({}) does not exist".format(transformation))
    return parameter


def priors(dependent, categ=None):
    if categ is None:
        categ = list(set(dependent))
    return [sum([cat == dep for cat in categ]) / len(dependent) for dep in dependent]


def sigmoid(Z):
    return 1. / (1. + np.exp(-Z))
