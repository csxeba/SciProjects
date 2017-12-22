import os

import numpy as np
import pandas as pd


projectroot = os.path.expanduser("~/SciProjects/Project_alcmodel/")


class Converter:

    DENSETOH = 0.789

    def __init__(self, model=None, data=None, deg=2):
        self.deg = deg
        self.data = Converter.get_reference() if data is None else data
        self.model = Converter.density_model(deg, self.data) if model is None else model

    @staticmethod
    def get_reference():
        return pd.read_excel(projectroot + "points.xlsx")

    @staticmethod
    def _fit_curve(X, Y, deg):
        return np.poly1d(np.polyfit(X, Y, deg=deg))

    @staticmethod
    def _plot_curves(X, Y, model, labels=None):
        from matplotlib import pyplot as plt
        pred = model(X)
        plt.plot(X, Y)
        plt.plot(X, pred)
        if labels:
            plt.xlabel(labels[0])
            plt.ylabel(labels[1])

        plt.grid()
        plt.show()

    @staticmethod
    def density_model(deg=2, data=None):
        data = Converter.get_reference() if data is None else data
        X, Y = data["VV"], data["DENSE"]
        return Converter._fit_curve(X, Y, deg)

    @staticmethod
    def weight_percent_model(deg=2, data=None):
        data = Converter.get_reference() if data is None else data
        X, Y = data["VV"], data["MM"]
        return Converter._fit_curve(X, Y, deg)

    def convert(self, points):
        X = points.as_matrix() if isinstance(points, pd.DataFrame) else points
        return self.model(X)

    def to_absalc(self, vperc, X):
        if not isinstance(vperc, np.ndarray):
            vperc = vperc.as_matrix().ravel()
        if not isinstance(X, np.ndarray):
            X = X.as_matrix()
        dens = self.model(vperc)[:, None]
        return (X * dens) / ((vperc * self.DENSETOH)[:, None]) * 100

    def plot(self, model=None):
        model = self.model if model is None else model
        X, Y = self.data["VV"], self.data["DENSE"]
        labels = ("V/V%", "Density @ 20°C")
        Converter._plot_curves(X, Y, model, labels)

    def plotw(self, deg=2):
        model = Converter.weight_percent_model(deg)
        X, Y = self.data["VV"], self.data["MM"]
        labels = ("V/V%", "Density @ 20°C")
        Converter._plot_curves(X, Y, model, labels)

    def __call__(self, points):
        return self.convert(points)
