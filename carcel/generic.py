def pull_data(crossval):
    from csxnet.data import CData
    from csxnet.nputils import import_from_csv
    from csxnet.utilities import roots

    table = import_from_csv(roots["csvs"] + "sum_ntab.csv", labels=7, sep="\t")
    data, labels, headers = table
    labels = labels[..., -1].astype("float32")

    data = CData((data[..., -11:], labels), cross_val=crossval)
    data.self_standardize()

    return data


def pull_samples():
    from csxnet.nputils import import_from_csv
    from csxnet.utilities import roots

    data, labels, headers = import_from_csv(roots["csvs"] + "3C6D.txt", sep="\t")

    return data, labels


