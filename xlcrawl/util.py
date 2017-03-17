import os

import openpyxl as xl
from openpyxl.worksheet import Worksheet


def iter_flz(root):
    for xlnm in (flnm for flnm in sorted(os.listdir(root)) if flnm[-5:] == ".xlsx"):
        xlwb = xl.load_workbook(xlnm)
        yield xlnm, xlwb.worksheets[0]


def walk_column_until(ws: Worksheet, coln: int, strval: str, limit=30, limitstr=""):
    strval = strval.lower()
    itr = next(ws.iter_cols(min_col=coln+1, max_col=coln+1, min_row=0, max_row=limit))
    for i, c in enumerate(itr):
        cval = str(c.value).lower()
        if strval in cval:
            return i+1
        if i >= limit:
            return None
        if limitstr:
            if limitstr in cval:
                return None


class DJ:

    def __init__(self, xlpath):
        self.djnames = {}
        self.munumbers = {}
        self.munames = {}
        djwb = xl.load_workbook(xlpath)
        for row in djwb.worksheets[0]:
            djnum = row[1].value
            if not isinstance(djnum, int):
                continue
            self.djnames[djnum] = row[2].value
            self.munumbers[djnum] = row[5].value
        # for row in djwb.worksheets[1]:
        #     self.munames[row[0].value] = row[1].value

    def dj_name_to_nums(self, name):
        return [k for k, v in sorted(self.djnames.items()) if name == v]

    def mu_to_dj(self, mu):
        return [k for k, v in sorted(self.munumbers.items()) if v == mu]
