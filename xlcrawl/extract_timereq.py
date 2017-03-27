import os

from openpyxl.worksheet import Worksheet

from SciProjects.xlcrawl import projectroot
from SciProjects.xlcrawl.util import iter_flz


def extract_ws(ws: Worksheet, flnm=None):

    def determine_starting_row():
        headingrow = None
        vizsgidrow = None
        for i, cell in enumerate(next(ws.columns), start=1):
            if "érköltség" in str(cell.value):
                headingrow = i
                break
            if i > 40:
                raise RuntimeError("Didn't find heading: Bérköltség")
        for i, cell in enumerate(next(ws.columns)[headingrow:], start=1):
            if "ideje" in str(cell.value):
                vizsgidrow = i
                break
            if i > 10:
                raise RuntimeError("Didn't find heading: Vizsgálat ideje")
        return headingrow + vizsgidrow

    def walk_throug_column(col, startrow=0):
        found = []
        for j, cl in enumerate(next(ws.iter_cols(col))[startrow:]):
            v = str(cl.value)
            if "perc" in v or "referens" in v or "alitika" in v:
                found.append(cl.value)
            if j > 10 or len(found) == 2:
                return found

    def extract_strings(startrow=0):
        for j in range(10):
            refstrings = walk_throug_column(j, startrow)
            if len(refstrings) == 2:
                return refstrings

    def extract_time_info_from_string(s):
        if s[-1] in "-:":
            return 0
        found = [int(s) for s in s.split() if s.isdigit()]
        if len(found) > 1:
            raise RuntimeError("Found multiple candidates in {}: ".format(flnm)
                               + ", ".join(map(str, found)))
        try:
            found = found[0]
        except IndexError:
            print(" No nums found in {}. Last char was [".format(flnm)+s[-1]+"]")
            found = 0
        return found

    def extract_names_from_string(s):
        if "(" not in s or ")" not in s:
            return
        start = s.find("(")+1
        stop = len(s) - s[::-1].find(")")-1
        slc = s[start:stop].replace("\n", " ").strip()
        return slc

    def handle_multiline(s, findstring):
        if "\n" in str(s):
            for ss in s.split("\n"):
                if findstring in ss:
                    return ss
            else:
                return s[0]
        else:
            return s

    start = determine_starting_row()
    strings = extract_strings(start)
    if strings is None:
        print("TIMEREQ: No valid string in {}".format(flnm))
        return [""]*4
    for i in range(len(strings)):
        strings[i] = handle_multiline(strings[i], ("szakreferens" if i else " referens"))
    timeinfos = list(map(extract_time_info_from_string, strings))
    nameinfos = list(map(extract_names_from_string, strings))
    return timeinfos + nameinfos


def main():
    os.chdir(project_root + "ALLXLFLZ")

    chain = "FILE\tMTIME\tTTIME\tMNAME\tTNAME\n"
    lndir = len(os.listdir("."))
    strln = len(str(lndir))
    for i, (flnm, ws) in enumerate(iter_flz("."), start=1):
        print("\rDoing file: {:>{w}}/{}".format(i, lndir, w=strln), end="")
        results = extract_ws(ws, flnm)
        chain += flnm + "\t"
        chain += "\t".join(map(str, results)) + "\n"

    print()

    with open(project_root + "timereq.csv", "w") as handle:
        handle.write(chain)
