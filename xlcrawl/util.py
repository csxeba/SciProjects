import openpyxl as xl


class DJ:
    def __init__(self, xlpath):
        self.gutter = [[None, None]]
        djwb = xl.load_workbook(xlpath)
        djws = djwb.worksheets[0]
        for row in djws.rows:
            iwant = (2, 5)
            line = []
            for i, cell in enumerate(row):
                if i == 0:
                    continue
                if i in iwant:
                    line.append(cell.value)
            self.gutter.append(line)

    def __getitem__(self, item, feature=None):
        if feature is None:
            return self.gutter[item]
        trdct = {"név": 0, "munkaut": 1}
        return self.gutter[item][trdct[feature]]
