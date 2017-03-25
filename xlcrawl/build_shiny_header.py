import os

import openpyxl as xl
from openpyxl.worksheet import Worksheet

from SciProjects.xlcrawl import shinyroot, project_root
from SciProjects.xlcrawl.util import DJ

djdb = DJ(project_root + "Díjjegyzék.xlsx")

ranges = {
    "djnum": "C1",
    "djname": "A4",
    "owner": "E6",
    "mname": "E9",
    "akknums": "E10",
    "mnum": "E11",
    "mernok": "A14",
    "mtasz": "C14",
    "mhour": "D14",
    "techn": "E14",
    "ttasz": "G14",
    "thour": "H14",
    "hmernok": "A16",
    "hmtasz": "C16",
    "htechn": "E16",
    "httasz": "G16",
}
destroot = shinyroot + "reparsed_head/"


def pull_data(flnm):
    data = {}
    with open(shinyroot + flnm) as handle:
        next(handle)  # skip header row
        for line in handle:
            line = line[:-1].split("\t")
            if line[0] in data:
                raise RuntimeError("Already in dictionary: " + line[0])
            data[line[0]] = line[1:]
    return data


def instantiate_template(flnm):
    newpath = destroot + flnm
    handle = xl.load_workbook(shinyroot + "head_template.xlsx")
    handle.save(newpath)
    return xl.load_workbook(newpath)


def assemble_header_data():

    def cell(rng, val):
        if isinstance(val, str):
            val = int(val) if val.isdigit() else val
        destws[ranges[rng]].value = val

    persolnell = pull_data("timereq.csv")
    dj = pull_data("djname.csv")
    for flnm in os.listdir(project_root + "ALLXLFLZ/"):
        print("Doing", flnm)
        tmplt = instantiate_template(flnm)  # type: xl.Workbook
        destws = tmplt.get_sheet_by_name("Adat")  # type: Worksheet
        mtime, ttime, mname, tname = persolnell.get(flnm, [""]*4)
        djread, djinfer, p = dj.get(flnm, [""]*3)
        if djread and djread.isdigit():
            djnum = djread
        else:
            if p and float(p) > 0.9:
                djnum = djinfer
            else:
                djnum = ""
        djname = djdb.djnames.get(int(djnum), "") if djnum else ""
        mnumber = djdb.munumbers.get(int(djnum), "") if djnum else ""
        cell("djnum", djnum)
        cell("djname", djname)
        cell("mnum", mnumber)
        cell("mname", djname)
        cell("mernok", mname)
        cell("mhour", mtime)
        cell("techn", tname)
        cell("thour", ttime)
        cell("owner", mname)
        tmplt.save(shinyroot + "reparsed_head/" + flnm)

if __name__ == '__main__':
    assemble_header_data()
