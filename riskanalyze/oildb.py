import os

import xlrd as xl

from SciProjects.riskanalyze import projectroot


dataroot = projectroot + "adat/"


def pull_headers(flnm):
    ws = xl.open_workbook(dataroot + flnm).sheet_by_index(0)
    return [flnm] + [ws.cell(2, i).value for i in range(ws.ncols)]


headers = [pull_headers(fl) for fl in os.listdir(dataroot) if fl[-3:] == "xls"]

with open("headers.csv", "w") as handle:
    handle.write("\n".join("\t".join(map(str, line)) for line in headers))
