def pull_data(crossval):
    from csxdata import CData, roots
    from csxdata.utilities.parser import parse_csv

    table = parse_csv(roots["csvs"] + "sum_ntab.csv", indeps=7)
    data, labels, headers = table
    labels = labels[..., -1].astype("float32")

    data = CData((data[..., -11:], labels), cross_val=crossval)
    data.transformation = "std"
    return data


def pull_samples():
    from csxdata import roots
    from csxdata.utilities.parser import parse_csv

    data, labels, headers = parse_csv(roots["csvs"] + "3C6D.txt", indeps=1)
    return data, labels
