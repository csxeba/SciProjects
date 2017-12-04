import os
projectroot = os.path.expanduser("~/SciProjects/Project_Sophie/")
axtitles = {"DHI": "$(D/H)_I$ (ppm)", "D13C": "$\\delta^{13}C$ (‰)"}


def pull_data(source, sep="\t"):
    from csxdata.parser import parser
    data, labels, header = parser.csv(projectroot + source, indeps=1, headers=1,
                                      dehungarize=True, decimal=True, sep=sep)
    X_C, Y_C, DHI, D13C = data.T
    CCode = labels[:, 0]

    return Y_C, DHI, D13C, CCode
