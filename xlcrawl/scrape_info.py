import os
from collections import defaultdict
from difflib import SequenceMatcher

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
    for nm in djnums:
        newstrlst += [s.replace(nm, " ").replace("  ", " ").replace("  ", "").strip()
                      for s in strlst]

    return tuple(map(sorted, map(list, map(set, (djn, djns, newstrlst)))))


def iter_flz(root):
    for xlnm in (flnm for flnm in sorted(os.listdir(root)) if flnm[-5:] == ".xlsx"):
        xlwb = xl.load_workbook(xlnm)
        yield xlnm, xlwb.worksheets[0]


if __name__ == '__main__':
    chain = ""
    numz = defaultdict(list)
    for flnm, ws in iter_flz("."):
        djn, djs, strs = extract_dj_number(ws, flnm)
        trflnm = (flnm[:-5]
                  .replace("NAV SZI", "")
                  .replace("NAVSZI", "")
                  .strip())
        for n in djn:
            numz[n].append(trflnm)
        chain += "-" * 50 + "\n"
        chain += flnm + "\n"
        chain += "STRINGZ: " + ", ".join(strs) + "\n"
        chain += "DJ_NUMZ: " + ", ".join((str(n) for n in djn)) + "\n"
        chain += "DJ_NUMS: " + ", ".join(djs) + "\n"
        chain += "-" * 50 + "\n"
    nice = (str("{}: {}".format(*it)) for it in sorted(numz.items(), key=lambda t: t[0]))
    print("DJns found:\n", "\n".join(nice))
    with open("../sum.txt", "w") as handle:
        handle.write(chain)

