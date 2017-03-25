import abc
import os

import numpy as np
import openpyxl as xl

from SciProjects.xlcrawl import project_root, shinyroot

srccateg = ("head", "chem", "inst", "item")
destroot = "/data/Ideglenessen/onkoltseg_output/"
# vbhvcfrcd  bh jn -- Ezt a Cuni írta :)


class Table(abc.ABC):

    categ = ""

    def __init__(self, filename, path, gutter):
        self.__dict__ = {k: v for k, v in locals().items() if k != "self"}

    @classmethod
    def extract(cls, flpath, dim, locator, extractor=None):
        flnm, path = cls._slicepath(flpath)

        ws = xl.load_workbook(flnm).worksheets[0]
        result = locator(ws, flnm)
        if not result:
            return cls(flnm, path, gutter=np.array([["-"]*dim]))
        if extractor is None:
            row, col, extractor = result
            data = extractor(ws, extractor, row, col, flnm)
        else:
            row, col = result
            data = extractor(ws, row, col, flnm)
        return cls(flnm, path, gutter=np.array(data))

    @classmethod
    def query(cls, source, flpath, dim):
        from SciProjects.xlcrawl.build_shiny_tables import Reorder
        flnm, path = cls._slicepath(flpath)
        with open(source) as handle:
            next(handle)  # skip header row
            data = [line for line in handle if line[0] == flnm]
            if data:
                data = np.array([Reorder.do(Reorder.tonice(line), dim) for line in data])
            else:
                data = np.array([["-"]*dim])
        return cls(flnm, path, gutter=data)

    @staticmethod
    def _slicepath(flpath):
        path = os.path.split(flpath)
        return os.path.join(path[:-1]), path[-1]


class ChemTable(Table):

    categ = "chem"

    @classmethod
    def extract_original(cls, flpath):
        from SciProjects.xlcrawl.extract_chemicals import (
            locate_table_header, extract_matrix
        )
        return ChemTable.extract(flpath, 4, locate_table_header, extract_matrix)


class ItemTable(Table):

    categ = "item"

    @classmethod
    def extract_original(cls, flpath):
        from SciProjects.xlcrawl.extract_items import (
            locate_table, extract_matrix
        )
        return ItemTable.extract(flpath, 3, locate_table, extract_matrix)


class InstTable(Table):

    categ = "inst"

    @classmethod
    def extract_original(cls, flpath):
        from SciProjects.xlcrawl.extract_instrument import (
            locate_table, extract_matrix
        )
        return ItemTable.extract(flpath, 3, locate_table, extract_matrix)


class HeaderData(Table):

    @classmethod
    def extract_original(cls, flpath):
        from SciProjects.xlcrawl.extract_timereq import extract_ws
        flnm, path = cls._slicepath(flpath)
        ws = xl.load_workbook(flpath).worksheets[0]
        timevec = extract_ws(ws)



class Method:

    def __init__(self, headerdata, chemtable, insttable, itemtable):
        self.__dict__ = {k: v for k, v in locals().items() if k != "self"}


def clear_workdirs():
    if input("Are you sure? [Y/n] > ").lower() == "n":
        return
    for fl in os.listdir(project_root + "ALLXLFLZ"):
        os.remove(fl)
    for categ in srccateg:
        for fl in shinyroot + "reparsed_" + categ:
            os.remove(fl)
