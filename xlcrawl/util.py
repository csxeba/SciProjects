from collections import defaultdict
import openpyxl as xl


class DJ:
    def __init__(self, xlpath):
        self.bydj = []
        self.bymu = defaultdict(list)
        djwb = xl.load_workbook(xlpath)
        for row in djwb.worksheets[0]:
            iwant = (2, 5)
            line = []
            for i, cell in enumerate(row):
                if i == 0:
                    continue
                if i in iwant:
                    line.append(cell.value)
            self.bydj.append(line)
        for row in djwb.worksheets[1]:
            self.bymu[row[0].value] = row[1].value

    def djname(self, item):
        return self.bydj[item][0]

    def tomu(self, item):
        return self.bydj[item][1]

    def navsziname(self, item):
        return self.bymu[item]
