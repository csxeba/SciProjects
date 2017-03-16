from collections import defaultdict
import openpyxl as xl


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
        for row in djwb.worksheets[1]:
            self.munames[row[0].value] = row[1].value

    def dj_name_to_nums(self, name):
        return [k for k, v in sorted(self.djnames.items()) if name == v]

    def mu_to_dj(self, mu):
        return [k for k, v in sorted(self.munumbers.items()) if v == mu]
