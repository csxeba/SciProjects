import pandas as pd

from SciProjects.vinyard import projectroot


DEFAULTPATH = projectroot + "BorAdatbázis.xlsx"


class WineData:

    _label = ["ID", "SAMPLER", "GRAPEQUANT", "CULTIVAR", "COLOUR",
              "WINEREGION", "WINECOUNTRY", "YEAR", "GEOORIGIN", "COUNTY"]
    _gps = ["GPSX", "GPSY", "GPSZ"]
    _sugar = ["BRIX", "GLU", "FRU", "SAC"]
    _alcohol = ["ETOH", "GLYC", "DISTETOH"]
    _physical = ["DENSITY", "DRYMATTER"]
    _acid = ["TOTALACID", "TRTA", "MLCA", "CTRA", "SCNA", "ACTA", "LCTA"]
    _isotope = ["DH1", "DH2", "D13C", "D18O"]
    _metal = ["K", "MG", "CU", "CA", "FE", "NA"]
    _indeps = _sugar + _alcohol + _physical + _acid + _isotope + _metal
    _columns = _label + _gps + _indeps

    def __init__(self):
        self.raw = None
        self._read_raw_data()
        self.loc = self.raw.loc
        self.iloc = self.raw.iloc

    def _read_raw_data(self):
        self.raw = pd.read_excel(DEFAULTPATH, sheet_name="DATA", index_col="EURODAT")[self._columns]

    def __getitem__(self, item):
        return self.raw[item]
