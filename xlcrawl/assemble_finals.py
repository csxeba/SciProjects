import os

import openpyxl as xl

from SciProjects.xlcrawl import projectroot
from SciProjects.xlcrawl.util import Allomany

ranges = {
    "mernok": "B14",
    "techni": "B19",
    "hmernok": "B17",
    "htechni": "B22"
}

personell = Allomany()


def inject_hpeople(xlwb: xl.Workbook, flnm):

    def correct(name):
        if name is None:
            return "-"
        name = name.strip()
        if name in ("-", ""):
            return "-"
        while name not in personell.data:
            if "Marusnikné" in name:
                return "Marusnikné Sárközi Ágnes"
            elif "Szabó Ferenc" in name:
                return "Szabó Ferenc"
            name = input("FURA @ {}\nKi ez? [{}] > ".format(flnm, name))
        return name

    def parse_helyettes(name):
        chainz = []
        h = personell.helyettes(name)
        hs = h.split("; ")
        for nm in hs:
            nm = correct(nm)
            tasz = personell.tasz(nm)
            chainz.append(f"{nm} ({tasz})")
        return ", ".join(chainz)

    head = xlwb.get_sheet_by_name("head")
    mernok = correct(head[ranges["mernok"]].value)
    technikus = correct(head[ranges["techni"]].value)
    print(mernok)
    print(technikus)
    print(parse_helyettes(mernok))
    print(parse_helyettes(technikus))
    # head[ranges["mernok"]] = mernok
    # head[ranges["techni"]] = technikus
    # head[ranges["hmernok"]] = parse_helyettes(mernok)
    # head[ranges["htechni"]] = parse_helyettes(technikus)


def printem(headws):
    djnum = headws["B4"].value
    djname = headws["B5"].value
    owner = headws["B6"].value
    print(str(djnum).lower()
          .replace(" ", "")
          .replace("none", "")
          .replace("nincs", "")
          .replace("-", ""), end="\t")
    print(djname, end="\t")
    print(owner)


def getdupers(headws):
    djnum = str(headws["B4"].value).strip()
    djname = headws["B5"].value
    owner = headws["B6"].value
    if "," in djnum:
        print(f"{owner}: {djnum}-{djname}")


def main():
    root = projectroot + "FINAL/"
    xlstream = (fl for fl in os.listdir(root) if fl[0] != "~" and fl[-5:] == ".xlsx")
    for flnm in xlstream:
        wb = xl.load_workbook(root + flnm)
        inject_hpeople(wb, flnm)
        # wb.save(root + flnm)


if __name__ == '__main__':
    main()
