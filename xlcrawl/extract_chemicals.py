import os

from SciProjects.xlcrawl import projectroot
from SciProjects.xlcrawl.util import walk_column_until, iter_flz
from openpyxl.worksheet import Worksheet


class RowExtractor:

    def __init__(self, evenodd, flnm):
        self.evenodd = evenodd
        self.flnm = flnm

    def __call__(self, ws, rown, startcol):
        data = self.extract_row(ws, rown, startcol)
        if data is None:
            return None
        if self.evenodd:
            data = self.separate_evenodd(data)
        return list(map(str, data))

    def extract_row(self, ws, rown, startcol):
        data = []
        coln = startcol
        while len(data) != (10 if self.evenodd else 5):
            found = ws.cell(row=rown, column=coln).value
            if found == "-":
                found = None
            data.append(str(found).strip() if found is not None else None)
            coln += 1
        if all(e is None for e in data):
            return
        if len(data) == 0:
            data = [[""]*5]
        return data

    def separate_evenodd(self, data):
        odd = data[::2]
        even = data[1::2]
        updated = []
        for i, (left, right) in enumerate(zip(odd, even), start=1):
            if (left is not None) and (right is not None):
                # if i == len(data) // 2:
                #     continue
                msg = ("CHEM-JAM in {}:\n{} <- this stays\n{}"
                       .format(self.flnm, left, right))
                print(msg)
            updated.append(left if left != "None" else right)
        return updated


def locate_table_header(ws: Worksheet, flnm):

    shouldbe = ["Vegyszer neve", "CAS száma", "Tisztasága", "Szükséges mennyiség", "Cikkszám"]

    def valid_header(got):
        if got is None:
            return False
        return all(left == right for left, right in zip(got, shouldbe))

    myrow = None
    coln = 0
    while myrow is None:
        myrow = walk_column_until(ws, coln, "vegyszer neve", limit=40)
        coln += 1
        if coln >= 20:
            return None
    extractor = RowExtractor(evenodd=False, flnm=flnm)
    header = extractor(ws, myrow, coln)
    if not valid_header(header):
        extractor = RowExtractor(evenodd=True, flnm=flnm)
        header = extractor(ws, myrow, coln)
        if not valid_header(header):
            msg = "CHEM: Invalid table header, assuming 'evenodd' @ " + flnm + " "
            print(msg)
    return myrow + 1, coln, extractor


def extract_matrix(ws: Worksheet, extractor, startrow, startcol, flnm):
    rown = startrow
    data = []
    ran = 0
    first_empty_row = 0
    lines_found = 0
    while 1:
        if ran > 50:
            print("CHEM: Overrun in {}.\nClipping back to {}!".format(flnm, first_empty_row))
            return data[:first_empty_row]
        col0 = str(ws.cell(row=rown, column=1).value)
        row = extractor(ws, rown, startcol)
        if "eszközök, műszerek" in col0:
            break
        ran += 1
        rown += 1
        if row is None:
            if not lines_found and ran > 1:
                first_empty_row = lines_found
            continue
        data.append(row)
        lines_found += 1
    return data


def assemble_chemtable():
    os.chdir(projectroot + "/ALLXLFLZ/")

    shouldbe = ["Vegyszer neve", "CAS száma", "Tisztasága", "Szükséges mennyiség", "Cikkszám"]

    lndir = len(os.listdir("."))
    strln = len(str(lndir))
    chain = "\t".join(["FILE"] + shouldbe) + "\n"
    for i, (flnm, ws) in enumerate(iter_flz("."), start=1):
        print("\rProgress: {:>{w}}/{} @ {}".format(i, lndir, flnm, w=strln), end="")
        result = locate_table_header(ws, flnm)
        if not result:
            chain += flnm + "\t" + "-\t" * len(shouldbe) + "\n"
            continue
        row, col, extractor = result
        data = extract_matrix(ws, extractor, row, col, flnm)
        if not data:
            chain += flnm + "\t" + "-\t" * len(shouldbe) + "\n"
            continue
        chain += "\n".join("\t".join(line) for line in data) + "\n"
    print()

    with open(projectroot + "chem.csv", "w") as handle:
        handle.write(chain.replace("None", "-"))
