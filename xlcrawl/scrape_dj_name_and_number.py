import os
from difflib import SequenceMatcher

import numpy as np
from openpyxl.worksheet import Worksheet

from SciProjects.xlcrawl import project_root
from SciProjects.xlcrawl.util import DJ, iter_flz

os.chdir(project_root + "ALLXLFLZ/")


def strsim(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()


def extract_djnum_easy(xlws: Worksheet):
    for cell in next(xlws.columns):
        cv = str(cell.value).lower()
        if "díjjegyzék száma:" in cv:
            cv = (cv
                  .replace(".", "")
                  .replace(":", "")
                  .replace("nav szi", "")
                  .replace("navszi", ""))
            try:
                return [int(d) for d in cv.split() if d.isnumeric()][0]
            except IndexError:
                return None


def split_string(s):

    def split_string_along_separators(val, seps):
        sepped = []
        for character in seps:
            sepped += val.split(character)
        return sepped

    candstrings = []
    separators = [".", ",", "-", "_"]
    for sp in separators:
        candstrings += split_string_along_separators(s, sp)
    candstrings = list(set((cnd for cnd in candstrings)))
    numbers = []
    for i in range(len(candstrings)):
        cand = candstrings.pop(0)
        for sp in separators + ["  ", "  "]:
            cand = cand.replace(sp, " ")
        cand = cand.strip()
        if cand.isdigit():
            numbers.append(int(cand))
        else:
            candstrings.append(cand)
    return candstrings, numbers


def infer_djnum_from_string(string, flnm):

    dj = DJ(project_root + "Díjjegyzék.xlsx")
    candidates = split_string(string)[0] + split_string(flnm)[0]
    refnumbers, refnames = zip(*sorted(dj.djnames.items(), key=lambda x: x[0]))
    ps = np.array([[strsim(rname, cnd) for cnd in candidates] for rname in refnames])
    refarg, candarg = np.unravel_index(ps.argmax(), ps.shape)
    return candidates[candarg], refnames[refarg], refnumbers[refarg], ps[refarg, candarg]


def extract_info(xlws: Worksheet, flnm):

    def reparse_methodnum(cellval):
        numbers = split_string(str(cellval))[1]
        numbers = list(set(numbers))
        if len(numbers) > 1:
            raise RuntimeError("Multiple candide method numbers @ {}:\n{}"
                               .format(flnm, ", ".join(numbers)))
        return numbers

    djname = None
    methodnum = None
    akkr = None
    found = False

    for i, cell in enumerate(next(xlws.columns)):
        if not found and str(cell.value) == "Díjjegyzék számítás":
            found = True
            continue
        if not found:
            continue

        if cell.value is None:
            continue

        if not djname:
            djname = cell.value
        elif djname and not methodnum:
            methodnum = reparse_methodnum(cell.value)
        elif methodnum and not akkr:
            v = str(cell.value).lower()
            if "akkred" in v:
                if v[:3] == "akk":
                    akkr = True
                elif v[:3] == "nem":
                    akkr = False
                else:
                    raise RuntimeError("Akkr is faulty in " + flnm)
            break
        if i >= 10:
            break

    return djname, methodnum, akkr


def main():
    lndir = len(os.listdir("."))
    strln = len(str(lndir))
    chain = "FILE\tFOUND\tDJN_READ\tMN_READ\tAKKR\tDJN_INFERRED\tDJNAME_INF\tP\n"
    for i, (flnm, ws) in enumerate(iter_flz("."), start=1):
        print("\rProgress: {:>{w}}/{} @ {}".format(i, lndir, flnm, w=strln), end="")
        djname, mn, ak = extract_info(ws, flnm)
        djnum = extract_djnum_easy(ws)
        cndnm, rfnm, rno, p = infer_djnum_from_string(djname, flnm)
        chain += "\t".join(map(str, (flnm, djname, djnum, mn, ak, rno, rfnm, p))) + "\n"

    with open(project_root + "djname.csv", "w") as handle:
        handle.write(chain)

if __name__ == '__main__':
    main()
