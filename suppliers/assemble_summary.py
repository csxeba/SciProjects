import pandas as pd

from SciProjects.suppliers import projectroot, resourceroot


def pull_ratings():

    def do1(filename, mode):
        frame = pd.read_excel(projectroot + filename)
        sups = pd.read_excel(resourceroot + "suppliers.xlsx")["SUPPLIER"].as_matrix()
        labels = ("N", "MIN", "IDŐ", "ÁR", "KAPCS", "TYAKM")
        data = {mode+l: [] for l in labels}
        for sup in sups:
            mask = frame["Beszállító"] == sup
            mu = frame.loc[mask, "Minőségi színvonal":].mean(axis=0).as_matrix()
            for l, d in zip(labels, [mask.sum()] + mu.tolist()):
                data[mode + l].append(d)
        return data

    output = do1("Merged_vegy.xlsx", "V")
    output.update(do1("Merged_eszk.xlsx", "E"))
    return output


def pull_headerdata():

    return pd.read_excel(projectroot + "Headerdata.xlsx", header=0, index_col=0)


def main():
    base = pull_headerdata()
    ratings = pull_ratings()
    for rating in ratings:
        base[rating] = ratings[rating]
    base.to_excel(projectroot + "Summary.xlsx")


if __name__ == '__main__':
    main()
