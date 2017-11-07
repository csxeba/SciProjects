import os

import xlrd as xl
import numpy as np
import pandas as pd

from SciProjects.suppliers import resourceroot, rawroot, projectroot


class SupData:

    def __init__(self, name, mID=None, boolvec=None, ratings=None):
        self.name = name
        self.mID = (set(), set()) if mID is None else mID
        self.boolvec = np.zeros(7).astype(bool) if boolvec is None else boolvec
        self.ratings = [] if ratings is None else ratings

    @property
    def meanrate(self):
        return self.ratings.mean(axis=0)

    @property
    def no_ratings(self):
        return len(self.ratings)

    @property
    def strline(self):
        akkpart = ", ".join(map(str, self.mID[0]))
        nakkpart = ", ".join(map(str, self.mID[1]))
        boolpart = "\t".join(map(lambda b: "X" if b else "", self.boolvec))
        # ratepart = "\t".join(np.mean(self.ratings, axis=0).astype(str))
        return "\t".join([self.name, nakkpart, akkpart, boolpart])

    def incorporate(self, other):
        self.mID[0].update(other.mID[0])
        self.mID[1].update(other.mID[1])
        self.boolvec |= other.boolvec
        self.ratings += other.ratings


def _reparse_mno(value):
    rprs = (str(value)
            .replace("nan", "")
            .replace(" ", "")
            .replace(".", "")
            .replace("NAVSZI-", "")
            .replace("NAVSZI", "")
            .replace(";", ","))
    return set([elem for elem in rprs.split(",") if elem not in ("", " ")])


def extract_wb(wb: xl.Book):
    df = pd.read_excel(wb, engine="xlrd", header=None, skiprows=4, names=col)
    ix = df["CÉG"]
    boolmat = df.loc[:, "MBESZ":].as_matrix().astype(str)
    boolmat[boolmat == "nan"] = "0"
    boolmat[boolmat != "0"] = "1"
    boolmat = boolmat.astype(int).astype(bool)
    methmat = df.loc[:, ("NAKKR", "AKKR")].as_matrix().astype(str)
    valid = boolmat.sum(axis=1).astype(bool) & (methmat[:, 0] != "nan")
    IDs = [[], []]
    for na, a in methmat[valid]:
        IDs[0].append(_reparse_mno(na))
        IDs[1].append(_reparse_mno(a))
    output = {}
    for name, mID, boolvec in zip(ix[valid], zip(*IDs), boolmat[valid]):
        output[name] = SupData(name, mID, boolvec)
    return output


col = "CÉG", "NAKKR", "AKKR", "MBESZ", "MKARB", "MKAL", "EBESZ", "VBESZ", "CRM", "JÁRTAS"
supres = pd.read_excel(resourceroot + "suppliers.xlsx")
suppliers = {k: SupData(k) for k in supres.iloc[:, 0]}


for xlfl in os.listdir(rawroot):
    if xlfl[-5:] != ".xlsx":
        continue
    print("Reading", xlfl)
    wb = xl.open_workbook(rawroot + xlfl)
    sups = extract_wb(wb)
    for supname, supobj in sups.items():
        suppliers[supname].incorporate(supobj)

outchain = "\t".join(col) + "\n"
outchain += "\n".join(suppliers[s].strline for s in sorted(suppliers))
with open(projectroot + "Suppliers.csv", "w") as handle:
    handle.write(outchain)
