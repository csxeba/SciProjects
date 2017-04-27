projectroot = "/home/csa/SciProjects/Project_Sophie/"
axtitles = {"DHI": "$(D/H)_I$ (ppm)", "D13C": "$\\delta^{13}C$ (‰)"}


def pull_data(source="01GEO.csv", sep="\t"):
    from csxdata.utilities.parsers import parse_csv
    data, labels, header = parse_csv(projectroot + source, indeps=2, headers=1,
                                     dehungarize=True, decimal=True, sep=sep)
    X_C, Y_C, DHI, D13C = data.T
    CCode = labels[:, 0]

    return X_C, Y_C, DHI, D13C, CCode
