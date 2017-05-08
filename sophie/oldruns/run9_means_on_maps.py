import numpy as np

from csxdata.utilities.vectorops import (
    split_by_categories, discard_NaN_rows
)

from SciProjects.sophie import pull_data, projectroot


def assemble_X(pnm):
    param = globals()[pnm]
    fP, fX, fY, flabel = discard_NaN_rows(param, X_C, Y_C, CCode)
    split = split_by_categories(flabel, np.stack((fP, fX, fY), axis=1))
    data = ["\t".join(("GEO", pnm, "X", "Y"))]
    for label, array in split.items():
        if len(array) > 0:
            mean = array.mean(axis=0)
        else:
            mean = array.mean(axis=0)
        data.append("\t".join([label] + mean.astype(str).tolist()))
    with open(projectroot + pnm + "_MEANS.csv", "w") as handle:
        handle.write("\n".join(data).replace(".", ","))
    print(pnm, "assembled!")


X_C, Y_C, DHI, D13C, CCode = pull_data("04GEO_full.csv", sep=";")
assemble_X("DHI")
assemble_X("D13C")
