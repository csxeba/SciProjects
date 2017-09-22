import os
import shutil
from datetime import datetime

import xlrd as xl
from xlrd.sheet import Sheet

from SciProjects.irms_assemble import projectroot

columnoffset = {"EA": 8, "GC": 10}


def get_ids_and_means(flnm):
    wb = xl.open_workbook(flnm)
    xlws = wb.sheet_by_index(0)  # type: Sheet

    cv = xlws.cell_value

    def find_date():
        for rown in range(5):
            if cv(rown, 0) == "Date:":
                try:
                    wsdate = xl.xldate_as_tuple(cv(rown, 2), wb.datemode)
                except TypeError:
                    break
                # print("DATE READ:", wsdate)
                return datetime(*wsdate)
        wsdate = [int(flnm[i:i+2]) for i in range(0, 6, 2)]
        # print("DATE GUESSED:", wsdate)
        return datetime(2000 + wsdate[0], *wsdate[1:])

    def find_header():
        for rown in range(10):
            if xlws.cell_value(rown, 2) in ("Identifier 1", "Azonosító"):
                # print(f"HEADER IS IN ROW {rown}")
                return rown
        else:
            raise RuntimeError(f"No header in {flnm}")

    def classify():
        if "ea" in flnm:
            dcls = "EA"
        elif "gc" in flnm:
            dcls = "GC"
        else:
            raise RuntimeError("Unclassifiable!")
        # print("CLASSIFIED AS", dcls)
        return dcls

    def extract_matrix():
        dcol = 2 + columnoffset[dclass]
        data = []
        nopes = 0
        row = headrown
        while 1:
            row += 1
            if row > 100:
                # print("ROW OVERRUN!")
                break
            try:
                dval = cv(row, dcol)
            except IndexError:
                # print("NO MORE ROWS!")
                break
            if dval == "":
                nopes += 1
                if nopes > 10:
                    # print("REACHED NOPES > 10")
                    break
                else:
                    continue
            nopes = 0
            if int(dval) >= 0:
                raise RuntimeError("Invalid value for delta 13 C!")
            data.append((dclass, date, cv(row, 2), dval))
        return data

    # print("LOOKING FOR DATE...")
    date = find_date()
    # print("LOOKING FOR HEADER...")
    headrown = find_header()
    # print("INFERING DCLASS...")
    dclass = classify()
    # print("EXTRACTING MATRIX...")
    matrix = extract_matrix()
    return matrix


if __name__ == '__main__':
    os.chdir(projectroot + "Current/")
    alldata = []
    for xlflnm in sorted(os.listdir(".")):
        if "~" in xlflnm:
            continue
        print(f"WORKING ON {xlflnm}")
        try:
            alldata += get_ids_and_means(xlflnm)
        except Exception as E:
            print("RELOCATING, RAISED", str(E))
            shutil.move(xlflnm, f"../NOPE/{xlflnm}")
        # print()

    bigchain = "\n".join("\t".join(map(str, line)) for line in alldata)
    os.chdir("..")
    with open("assembled.csv", "w") as handle:
        handle.write(bigchain)
