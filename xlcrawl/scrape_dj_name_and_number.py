import os

import numpy as np
from openpyxl.worksheet import Worksheet

from SciProjects.xlcrawl import projectroot
from SciProjects.xlcrawl.util import (
    DJ, iter_flz, walk_column_until, strsim, striters
)


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

    dj = DJ(projectroot + "Díjjegyzék.xlsx")
    candidates = np.array(split_string(string)[0] + split_string(flnm)[0])
    refnumbers, refnames = zip(*sorted(dj.djnames.items(), key=lambda x: x[0]))
    refnumbers, refnames = tuple(map(np.array, (refnumbers, refnames)))
    ps = np.array([[strsim(rname, cnd) for cnd in candidates] for rname in refnames])
    args = np.argwhere(np.greater(ps, 0.9))
    args = args[np.argsort(ps[args[:, 0], args[:, 1]])[::-1]]
    refarg, candarg = args.T
    return candidates[candarg], refnames[refarg], refnumbers[refarg], ps[refarg, candarg]


def walk_columns(xlws: Worksheet, flnm):
    for colno in range(0, 10):
        rowno = walk_column_until(xlws, colno, "Díjjegyzék számítás", limit=15)
        if rowno is not None:
            header_start = [rowno, colno]
            break
    else:
        raise RuntimeError("'Díjjegyzék számítás' not found in " + flnm)

    rown, coln = header_start
    coln += 1
    offset = 1
    limit = 5
    while 1:
        djname = xlws.cell(row=rown+offset, column=coln).value
        offset += 1
        if (djname is not None) or (offset >= limit):
            break
    if djname is None:
        raise RuntimeError("DJSCRAPE: no valid djname in " + flnm)

    cells = tuple(xlws.iter_cols(min_col=coln, max_col=coln,
                                 min_row=rown+2, max_row=rown+12))[0]
    mname, akkr = None, None
    for cell in cells:
        if cell.value is None:
            continue
        cv = str(cell.value)
        if akkr is None and \
                ("Mérési módszer:" == cv[:15] or
                 "NAV SZI" in cv or "NAVSZI" in cv):
            mname = cv
        if mname is None and \
                ("akkred" in cv):
            akkr = cv
        if mname is not None and akkr is not None:
            break

    if not mname and "\n" in djname:
        print(" !!! DJSCRAPE: found newline @", flnm)
        sentences = djname.split("\n")
        for i, snt in enumerate(sentences):
            if "módszer" in snt.lower():
                djname = " ".join(sentences[:i])
                mname = " ".join(sentences[i:])
                break

    return striters((djname, mname, akkr))


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
    os.chdir(project_root + "ALLXLFLZ")
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
