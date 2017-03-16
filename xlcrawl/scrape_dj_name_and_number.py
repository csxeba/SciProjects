import os
from collections import defaultdict
from difflib import SequenceMatcher

import numpy as np
import openpyxl as xl
from openpyxl import worksheet

from SciProjects.xlcrawl import project_root
from SciProjects.xlcrawl.util import DJ

os.chdir(project_root + "ALLXLFLZ/")

dj = DJ(project_root + "Díjjegyzék.xlsx")


def strsim(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()


def extract_dj_number(xlws: worksheet.Worksheet, wbname=None):

    def try1(val, sep):
        return reparse(val.split(sep))

    def tryall(val, seps):
        sepped = []
        for sp in seps:
            sepped += val.split(sp)
        return reparse(list(set(sepped)))

    def reparse(lst):
        foundnum, foundnums, foundstring = [], [], []
        for d in lst:
            d = (d
                 .replace(".", " ")
                 .replace(",", " ")
                 .replace("-", " ")
                 .replace("_", " ")
                 .replace("  ", " ")
                 .replace("  ", " ")
                 .strip())
            try:
                foundnum.append(int(d))
            except ValueError or AttributeError:
                foundstring.append(d)
            else:
                foundnums.append(d)
        return foundnum, foundnums, foundstring

    cellval = None
    found = False
    for cell in next(xlws.columns):
        if found:
            if cell.value is not None:
                cellval = cell.value
                break
        elif str(cell.value) == "Díjjegyzék számítás":
            found = True

    djn, djns, strlst = [], [], []
    for sp in (".", ",", "-", "_"):
        if cellval is not None:
            djnum, djnums, strz = try1(cellval, sp)
            djn += djnum
            djns += djnums
            strlst += strz
            djnum, djnums, strz = tryall(cellval, sp)
            djn += djnum
            djns += djnums
            strlst += strz

        djnum, djnums, strz = try1(wbname[:-5], sp)
        djn += djnum
        djns += djnums
        strlst += strz
        djnum, djnums, strz = tryall(wbname[:-5], sp)
        djn += djnum
        djns += djnums
        strlst += strz

    newstrlst = []
    for nm in djns:
        newstrlst += [s.replace(nm, " ").replace("  ", " ").replace("  ", "").strip()
                      for s in strlst]

    return tuple(map(sorted, map(list, map(set, (djn, djns, newstrlst)))))


def iter_flz(root):
    for xlnm in (flnm for flnm in sorted(os.listdir(root)) if flnm[-5:] == ".xlsx"):
        xlwb = xl.load_workbook(xlnm)
        yield xlnm, xlwb.worksheets[0]


def infer_name(candidates):
    scores = []
    for cnd in candidates:
        scores.append([strsim(cnd, r) for r in dj.djnames.values()])
    scores = np.array(scores)
    arg = np.unravel_index(np.argmax(scores), scores.shape)
    bestcand = candidates[arg[0]]
    bestref = dj.djnames[arg[1]]
    return bestcand, bestref, scores[arg]

if __name__ == '__main__':
    chain = "FILE\tALLCND\tBESTC\tBESTR\tpR\tDJNCAND->\n"
    numz = defaultdict(list)
    ln = len(os.listdir("."))
    strln = len(str(ln))
    for i, (flnm, ws) in enumerate(iter_flz("."), start=1):
        print("\rDoing file {:>{w}}/{}".format(i, ln, w=strln), end="")
        djn, djs, strs = extract_dj_number(ws, flnm)
        trflnm = (flnm[:-5]
                  .replace("NAV SZI", "")
                  .replace("NAVSZI", "")
                  .strip())
        for n in djn:
            numz[n].append(trflnm)
        bc, br, p = infer_name(strs + [trflnm])
        addths = "\t".join((flnm,
                            "{" + "}, {".join(strs + [trflnm]) + "}",
                            bc, br, "{:>.4f}".format(p),
                           *[str(d) for d in dj.dj_name_to_nums(br)]))
        chain += addths + "\n"
    # nice = (str("{}: {}".format(*it)) for it in sorted(numz.items(), key=lambda t: t[0]))
    # print("DJns found:\n", "\n".join(nice))
    with open("../sum.csv", "w") as handle:
        handle.write(chain)
