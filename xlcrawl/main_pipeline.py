import os

import numpy as np
import openpyxl as xl
from openpyxl.worksheet import Worksheet

from SciProjects.xlcrawl import project_root, templateroot
from SciProjects.xlcrawl.util import extract_inventory_numbers, iter_flz

# vbhvcfrcd  bh jn -- Ezt a Cuni írta :)


def _slicepath(flpath):
    return os.path.split(flpath)


class NamelessAbstraction:

    templates = {
        c: templateroot + c + "_template.xlsx"
        for c in ("chem", "item", "inst", "head")
        }

    def __init__(self, path, flnm, categ, data):
        self.path = path
        self.flnm = flnm
        self.categ = categ
        self.data = data
        self.reparsed = None
        self.flpath = path + "/" + categ + "/" + flnm

    def instantiate_template(self):
        newpath = f"{self.path}/{self.categ}/"
        try:
            os.makedirs(newpath)
        except FileExistsError:
            pass
        handle = xl.load_workbook(self.templates[self.categ])
        handle.save(newpath + self.flnm)
        return xl.load_workbook(newpath + self.flnm)


class Table(NamelessAbstraction):

    """
    Raw extracted data is shaped like this:
    CHEM: NAME; CAS; PURITY; QUANT; INVNUM
    ITEM: NAMESTRING (INVNUM); QUANT
    INST: NAMESTRING (INVNUM); QUANT?

    Reparsed data is shaped like this:
    CHEM: INVNUM; NAME; QUANT_UNIT; QUANT_USED
    ITEM: INVNUM; NAME; QUANT_USED
    INST: INVNUM; NAME; SN; QUANT_USED
    """

    def __init__(self, data, path, flnm, categ):
        super().__init__(path, flnm, categ, data)
        self.dim = 3 if categ == "item" else 4
        if isinstance(data, Worksheet):
            self.read_data(data)
            self.reparse_data()

    def empty(self):
        self.data = [["-"] * (5 if self.categ == "chem" else 2)]

    def read_data(self, ws):
        locator, extractor = self._get_parsers()
        result = locator(ws, self.flnm)
        if not result:
            self.empty()
            return
        if len(result) > 2:
            row, col, extrobj = result
            self.data = extractor(ws, extrobj, row, col, self.flnm)
        else:
            row, col = result
            self.data = extractor(ws, row, col, self.flnm)
        if not len(self.data):
            self.empty()

    def reparse_data(self):
        rp = []
        for line in self.data:
            if not line:
                continue
            if self.categ == "chem":
                units = line[3].split(" ")
                quant = units[0].replace(",", ".")
                try:
                    quant = str(float(quant)).replace(".", ",")
                except ValueError:
                    quant = line[3]
                    unit = ""
                else:
                    unit = " ".join(units[1:])
                repline = [line[4], line[0], unit, quant]
            else:
                cand, refname = extract_inventory_numbers(line[0])
                if len(line) > 1:
                    qnt = line[1]
                else:
                    qnt = ""
                repline = ["/".join(cand), refname, qnt]
                if self.categ == "inst":
                    repline.insert(2, "")
            rp.append(repline)
        if not rp:
            rp = [[""]*(4 if self.categ == "chem" else 3)]
        self.reparsed = np.array(rp)

    def _get_parsers(self):
        if self.categ == "chem":
            from SciProjects.xlcrawl.extract_chemicals import (
                locate_table_header as locator,
                extract_matrix as extractor
            )
        elif self.categ == "item":
            from SciProjects.xlcrawl.extract_items import (
                locate_table as locator,
                extract_matrix as extractor
            )
        else:
            from SciProjects.xlcrawl.extract_instrument import (
                locate_table as locator,
                extract_matrix as extractor
            )
        return locator, extractor

    def dump(self):
        if self.reparsed is None:
            msg = " ".join(("Attempting to dump unreparsed", self.categ, "data"))
            raise RuntimeError(msg)
        template = self.instantiate_template()
        Xn, Yn = self.reparsed.shape
        ws = template.get_sheet_by_name("Adat")
        cellz = np.array(list(ws.iter_rows(
            min_row=6, max_row=5 + Xn, min_col=1, max_col=Yn
        )))
        for c, d in zip(cellz.ravel(), self.reparsed.ravel()):
            d = str(d).replace("None", "").replace("-", "")
            c.value = int(d) if d.isdigit() else d
        template.save(f"{self.path}/{self.categ}/{self.flnm}")


class Header(NamelessAbstraction):
    """
    The header consists of the following fields:
    [mtime, ttime, mname, tname, djnum, djname, mnum, mname]
    """

    ranges = {
        "djnum": "C1", "djname": "A4", "owner": "E6",
        "mname": "E9", "akknums": "E10", "mnum": "E11",
        "mernok": "A14", "mtasz": "C14", "mhour": "D14",
        "techn": "E14", "ttasz": "G14", "thour": "H14",
        "hmernok": "A16", "hmtasz": "C16", "htechn": "E16",
        "httasz": "G16"
    }

    def __init__(self, data, path, flnm):
        super().__init__(path, flnm, "head", data)
        if isinstance(data, Worksheet):
            self.data = self.get_timereq_data(data, flnm)
            self.data.extend(self.get_dj_data(data, flnm))
            self.reparsed = self.data

    @staticmethod
    def get_timereq_data(ws, flnm):
        from SciProjects.xlcrawl.extract_timereq import extract_ws
        return list(extract_ws(ws, flnm))

    @staticmethod
    def get_dj_data(ws, flnm):
        from SciProjects.xlcrawl.util import DJ
        from SciProjects.xlcrawl.scrape_dj_name_and_number import (
            walk_columns, extract_djnum_easy, infer_djnum_from_string
        )
        djname, mname, akkr = walk_columns(ws, flnm)
        djnum = extract_djnum_easy(ws)
        if djnum is None:
            cands, rfnames, djnums, ps = infer_djnum_from_string(djname, flnm)
            for djnum in djnums:
                if str(djnum) in djname:
                    break
            else:
                if djnum:
                    djnum = djnums[0]
                    djname = rfnames[0]
                else:
                    return [""]*4
        djdb = DJ(project_root + "Díjjegyzék.xlsx")
        mnum = djdb.munumbers[djnum]
        mname = djname
        return [djnum, djname, mnum, mname]

    def dump(self):
        def cell(rng, val):
            if isinstance(val, str):
                val = int(val) if val.isdigit() else val
                val = "" if val.lower() == "none" else val
            if val is None:
                val = ""
            ws[self.ranges[rng]].value = val

        handle = self.instantiate_template()
        mtime, ttime, owner, tname, djnum, djname, mnum, mname = self.data

        ws = handle.get_sheet_by_name("Adat")
        cell("djnum", djnum)
        cell("djname", djname)
        cell("mnum", mnum)
        cell("mname", djname)
        cell("mernok", owner)
        cell("mhour", mtime)
        cell("techn", tname)
        cell("thour", ttime)
        cell("owner", owner)
        handle.save(f"{self.path}/{self.categ}/{self.flnm}")


class Method:

    def __init__(self, flpath, ws=None):
        path, flnm = _slicepath(flpath)
        if not ws:
            xlin = xl.load_workbook(flpath)
            self.ws = xlin.worksheets[0]
        else:
            self.ws = ws
        self.sanity_check()
        self.head = Header(self.ws, path, flnm)
        self.chem = Table(self.ws, path, flnm, "chem")
        self.inst = Table(self.ws, path, flnm, "inst")
        self.item = Table(self.ws, path, flnm, "item")

    def sanity_check(self):
        return "Melléklet" in (self.ws["A1"].value, self.ws["A2"].value)

    def dump(self, newroot):
        os.chdir(newroot)
        self.head.dump()
        self.chem.dump()
        self.item.dump()
        self.inst.dump()


def cleanup(dstroot, force=False):
    import shutil
    msg = "\n".join(("You are attempting to empty the directory:",
                     dstroot,
                     "Are you sure? [yes] > "))
    if not force:
        if input(msg) != "yes":
            return
    for entry in os.listdir(dstroot):
        if os.path.isfile(entry):
            os.remove(dstroot + "/" + entry)
        else:
            shutil.rmtree(dstroot + "/" + entry)


def crawl(destination, source=project_root):
    cleanup(destination)

    for xlworksheet, xlpath in iter_flz(source):
        method = Method(xlpath, xlworksheet)
        method.dump(destination)

if __name__ == '__main__':
    destroot = "/home/csa/Ideglenessen/onkoltseg_output/"
    crawl(destroot)
