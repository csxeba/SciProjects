import os
import pickle as pkl
from collections import defaultdict

import numpy as np
import pandas as pd
import openpyxl as xl

from openpyxl.worksheet import Worksheet
from SciProjects.xlcrawl import projectroot

finalzroot = projectroot + "FIN/"
pklroot = projectroot + "methodpklz/"

ranges = {
    "djnum": "4", "djname": "5", "owner": "6",
    "mname": "9", "akknums": "10", "mnum": "11",
    "mernok": "14", "mtasz": "15", "mhour": "16",
    "hmernok": "17",
    "techn": "19", "ttasz": "20", "thour": "21",
    "htechn": "22",
    "vnumstr": "25"
}
ranges = {k: "B" + v for k, v in ranges.items()}


class Header:

    def __init__(self, ws: Worksheet):
        self.data = np.array([
            ws[c].value for c in sorted(ranges.values(), key=lambda v: int(v[1:]))
        ])


class Method:

    ids = set()
    nxts = defaultdict(int)

    def __init__(self, path, flnm):
        self.path = path
        self.flnm = flnm
        self.source = path + flnm
        wb = xl.load_workbook(path + flnm, data_only=True)
        self.head = Header(wb["head"])
        tabs = pd.read_excel(
            path+flnm, sheetname=["chem", "item", "inst"], header=4
        )
        self.__dict__.update(tabs)
        self.id = flnm.split("-")[0].zfill(3)
        if self.id in Method.ids:
            Method.nxts[self.id] += 1
            self.id += f"-{Method.nxts[self.id]:02d}"
        Method.ids.add(self.id)

    def headrow(self):
        return "\t".join(map(str, self.head.data))

    def tabpart(self, which):
        tab = self.__dict__[which].as_matrix()
        return "\n".join("\t".join([self.id] + list(map(str, line.tolist())))
                         for line in tab if not np.all(np.isnan(line)))

    @staticmethod
    def load(pklpath):
        with open(pklpath, "rb") as handle:
            return pkl.load(handle)


def print1():
    flnm = "101-Denaturálószerek meghatározása hamisított szeszesitalokból.xlsx"
    meth = Method(finalzroot, flnm)
    print(meth.headrow())
    print("CHEM:")
    print(meth.tabpart("chem"))
    print("ITEM:")
    print(meth.tabpart("item"))
    print("INST:")
    print(meth.tabpart("inst"))


def dumpchain(chain, fl):
    with open(fl, "w") as handle:
        handle.write(chain)


def main():
    methods = Method.load(pklroot + "methodmap.pkl")
    headchain = "MID\tDJNO\tDJNM\tOWNER\tMNM\tAKN\tMNO\tMNAME\t" +\
                "MTASZ\tMTIME\tMHSTR\tTNAME\tTTASZ\tTTIME\tTHSTR\n"
    chemchain = "MID\tIID\tCHEM\tUNIT\tQUANT\n"
    itemchain = "MID\tIID\tITEM\tQUANT\n"
    instchain = "MID\tIID\tINST\tSNO\tQUANT\n"

    pklz = os.listdir(pklroot)
    nflz = len(pklz)
    strln = len(str(pklz))
    for i, pklfl in enumerate(pklz, start=1):
        print("\r{:>{w}}/{}".format(i, nflz, w=strln), end="")
        mth = Method.load(pklroot + pklfl)
        methods[mth.id] = mth
        headchain += mth.id + "\t" + mth.headrow() + "\n"
        chemchain += mth.tabpart("chem") + "\n"
        itemchain += mth.tabpart("item") + "\n"
        instchain += mth.tabpart("inst") + "\n"

    print("Dumpin...")
    dumpchain(headchain, projectroot + "sum_head.csv")
    dumpchain(chemchain, projectroot + "sum_chem.csv")
    dumpchain(instchain, projectroot + "sum_inst.csv")
    dumpchain(itemchain, projectroot + "sum_item.csv")


if __name__ == '__main__':
    main()
