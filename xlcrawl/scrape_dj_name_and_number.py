import os
from collections import defaultdict
from difflib import SequenceMatcher

from openpyxl.worksheet import Worksheet

from SciProjects.xlcrawl import project_root
from SciProjects.xlcrawl.util import DJ, iter_flz

os.chdir(project_root + "ALLXLFLZ/")

dj = DJ(project_root + "Díjjegyzék.xlsx")


def strsim(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()


def extract_djname_easy(xlws: Worksheet):
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


def extract_djname_methodnumber_akkr(xlws: Worksheet, wbname=None):

    def try1(val, sep):
        return reparse_djname(val.split(sep))

    def tryall(val, seps):
        sepped = []
        for sp in seps:
            sepped += val.split(sp)
        return reparse(list(set(sepped)))

    def cell_extraction_logic():
        djname = None
        methodnum = None
        akkr = None
        found = False
        successive_empties = 0
        interesting_finds = 0

        for cell in next(xlws.columns):
            if not found and str(cell.value) == "Díjjegyzék számítás":
                found = True
                continue
            if not found:
                continue

            if cell.value is None:
                successive_empties += 1
                if successive_empties > 3:
                    break
                else:
                    continue

            if not interesting_finds:
                djname = cell.value
            elif interesting_finds == 1:
                methodnum = reparse_methodnum(cell.value)
            elif interesting_finds == 2:
                v = str(cell.value).lower()
                if "akkred" in v:
                    akkr = "nem" in v
            if successive_empties > 3 or interesting_finds > 2:
                break

            interesting_finds += 1
            successive_empties = 0

        return djname, methodnum, akkr

    def reparse_djname(lst):
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

    def reparse_methodnum(cellval):
        mn = None
        v = str(cellval).lower()
        if any(x in v for x in ("módszer", "nav", "navszi", "nav szi")):
            mn = (v
                         .replace("navszi", " ")
                         .replace("nav szi", " ")
                         .replace(".", " ")
                         .replace("mérési módszer", " ")
                         .replace(":", " ")
                         .replace(" ", ""))
            try:
                mn = int(mn)
            except ValueError:
                print("Can't INTify", mn)
        return mn

    def extract_djnumber_candidates():
        djnumber, djn_asstr, candstrings = [], [], []
        for sp in (".", ",", "-", "_"):
            if djname is not None:
                djnum, djnums, strz = try1(djname, sp)
                djnumber += djnum
                djn_asstr += djnums
                candstrings += strz
                djnum, djnums, strz = tryall(djname, sp)
                djnumber += djnum
                djn_asstr += djnums
                candstrings += strz

            djnum, djnums, strz = try1(wbname[:-5], sp)
            djnumber += djnum
            djn_asstr += djnums
            candstrings += strz
            djnum, djnums, strz = tryall(wbname[:-5], sp)
            djnumber += djnum
            djn_asstr += djnums
            candstrings += strz
        return djnumber, djn_asstr, candstrings

    djname, methodnum, akkr_status = cell_extraction_logic()
    djn, djns, strlst = tuple(map(sorted, map(list, map(set, (extract_djnumber_candidates())))))

    newstrlst = []
    for nm in djns:
        newstrlst += [s.replace(nm, " ").replace("  ", " ").replace("  ", "").strip()
                      for s in strlst]

    return djn, djns, strlst


def main():
    chain = ""
    numz = defaultdict(list)
    for flnm, ws in iter_flz("."):
        djnumber = extract_djname_easy(ws)
        djn, djs, strs = extract_djname_methodnumber_akkr(ws, flnm)
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
