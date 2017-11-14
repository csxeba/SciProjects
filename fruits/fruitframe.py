import numpy as np
import pandas as pd

from ..alcmodel import Converter
from . import projectroot


class FruitData:

    _isotope = ["DH1", "DH2", "D13C"]
    _volatile = ["METOH", "ACALD", "ETAC", "ACETAL", "1PROP", "2M1P", "2M1B", "3M1B"]
    _simplevol = ["METOH", "ACALD", "ETAC", "ACETAL", "1PROP", "2M1P", "AMYL"]
    _etoh = ["ALK"]
    _independent = _isotope + _etoh + _simplevol
    _transformation = [""] * 3 + ["exp"] + ["log"] * 7
    _dependent = ["FAMILIA", "GYUM", "EV"]
    _header = _dependent + _independent

    def __init__(self, transform=False):
        self.raw = None
        self.valid = None
        self.density_model = Converter(deg=3)

        self._read_raw_data(transform)
        self._cast_to_absolute_ethanol()
        if transform:
            self._apply_transformations()

        self.loc = self.valid.loc
        self.iloc = self.valid.iloc

    @property
    def X(self):
        return self.valid[self._independent]

    @property
    def Y(self):
        return self.valid[self._dependent]

    @property
    def isotope(self):
        return self.valid[self._isotope]

    @property
    def volatile(self):
        return self.valid[self._simplevol]

    def _read_raw_data(self, transform):
        df = pd.read_excel(projectroot + "adat.xlsx", index_col="EURODAT")  # type: pd.DataFrame
        self.raw = df[self._dependent + self._isotope + self._etoh + self._volatile].dropna()
        if transform:
            mask = np.zeros(len(self.raw), dtype=bool)
            for col in self.raw[self._volatile].as_matrix().T:
                mask |= col == 0.
            self.raw = self.raw[~mask]

    def _cast_to_absolute_ethanol(self):
        labels = self.raw[self._dependent]
        isotope = self.raw[self._isotope]  # type: pd.DataFrame
        ethanol = self.raw[self._etoh]
        volatile = self.raw[self._volatile]
        volatile["AMYL"] = volatile["2M1B"] + volatile["3M1B"]
        del volatile["2M1B"], volatile["3M1B"]
        cast = self.density_model.to_absalc(ethanol, volatile)
        aavol = pd.DataFrame(data=cast, index=volatile.index, columns=self._simplevol)
        self.valid = pd.concat([labels, isotope, ethanol, aavol], axis=1, join="inner", join_axes=[labels.index])

    def _apply_transformations(self):
        self.valid.loc[:, ("ALK", "METOH")] /= self.valid.loc[:, ("ALK", "METOH")].max(axis=0)
        for i, (col, trf) in enumerate(zip(self._independent, self._transformation)):
            if not trf:
                continue
            self.valid[col] = {"log": np.log, "exp": np.exp}[trf](self.valid[col])
        new_indeps = [f"{trf}({k})" if trf else k for k, trf in zip(self._independent, self._transformation)]
        new_columns = self._dependent + new_indeps
        self.valid.columns = new_columns
        self._simplevol = new_indeps[3:]
        self._independent = new_indeps
        self._header = new_columns

    def __getitem__(self, item):
        return self.valid[item]
