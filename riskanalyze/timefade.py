from datetime import datetime

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from shapefile import Reader

from csxdata import roots
from csxdata.utilities.vectorop import split_by_categories, rescale, downscale

from SciProjects.riskanalyze.utils import pull_data

# data header: RENDSZAM	SZOLGHELY	DATUM	HELY	MINTA	MEGF


def _time_scatter(xy, args, mpl_obj):
    if len(args) < 0:
        return 0
    mpl_obj.set_offsets(xy[args])
    return 1


class WindowedPlot:

    def __init__(self, filename):
        self.xy, self.data = pull_data(filename)
        self.dates, self.valid = self.data[:, 2], self.data[:, 5]
        self.dates = np.array([s.replace(".", "-") for s in self.dates], dtype="datetime64[D]")
        # self.hun = np.array(Reader(roots["gis"] + "hun/HUN_adm0.shp").shapes()[0].points)
        # self.hun, dfctr, ufctr = featscale(self.hun, return_factors=True)
        # self.rxy = downscale(self.xy, *dfctr)

    @property
    def sxy(self):
        return split_by_categories(self.valid, self.xy)

    def select(self, begin, end,):
        mask = np.logical_and(self.dates >= begin, self.dates <= end)
        return self.xy[mask], self.dates[mask], self.valid[mask]

    def get_current_points(self, begin, end):
        xy, dates, valid = self.select(begin, end)
        if not len(xy):
            return [], [], [], []
        splitargs = split_by_categories(valid)
        ages = (end - dates).astype(float)[::-1]
        ages /= ages.max()
        iargs = splitargs.get("0", [])
        vargs = splitargs.get("1", [])
        return xy, ages, iargs, vargs

    @staticmethod
    def time_scatter_invalid(xy, ages, args, mpl_obj):
        if not _time_scatter(xy, args, mpl_obj):
            return
        szs = (1.5 * (ages[args]+1))**5
        mpl_obj.set_sizes(szs)

    @staticmethod
    def time_scatter_valid(xy, ages, args, mpl_obj):
        del ages
        if not _time_scatter(xy, args, mpl_obj):
            return

    def init_heatmap(self, ax):
        hm, xe, ye = np.histogram2d(self.rxy[:, 0], self.rxy[:, 1], bins=100)
        hm /= hm.max()
        obj = ax.imshow(hm, extent=(xe[0], xe[-1], ye[0], ye[-1]),
                        vmin=0, vmax=1)
        return obj

    @staticmethod
    def heatmap_valid(xy, ages, args, mpl_obj):
        # w = (1.5 * ages[args]+1) ** 4  # type: np.ndarray
        hm, xe, ye = np.histogram2d(xy[args, 0], xy[args, 1], bins=100, weights=ages)
        mpl_obj.set_data(hm)

    def slide(self, start, window_size, step=1):
        end = self.dates.max()
        while start + window_size < end:
            xy, ages, iargs, vargs = self.get_current_points(start, start + window_size)
            yield xy, ages, iargs, vargs, start
            start += step

    def efficiency_curve(self, windowsize=30):
        pointstream = self.slide(self.dates.min(), windowsize, 1)
        eff = []
        hits = []
        actions = []
        xs = []
        ravg_eff = []
        running_sum = None
        gamma = (windowsize-1) / windowsize
        for xy, ages, iargs, vargs, start in pointstream:
            lxy = len(xy)
            if not lxy:
                continue
            eff.append(len(iargs) / lxy)
            if running_sum is None:
                running_sum = eff[-1]
            else:
                running_sum = gamma * running_sum + (1. - gamma) * eff[-1]
            xs.append(start)
            hits.append(len(iargs))
            actions.append(len(xy))
            ravg_eff.append(running_sum / windowsize)

        eff, hits, actions = list(map(np.array, (eff, hits, actions)))
        xs = np.array(xs, dtype="datetime64").astype(datetime)
        fig, ax = plt.subplots(2, 1, figsize=(12, 8))

        ax[0].plot(xs, hits, "r-", label="Fogások")
        ax[0].plot(xs, actions, "b-", label="Kiszállások")
        ax[0].set_title(f"Kiszállások és találatok száma\n({windowsize} napos időablak)")
        ax[0].set_ylabel("Események száma")
        ax[0].legend(loc="upper right")
        ax[0].grid(True, which="major", color="grey", linestyle="-")
        ax[0].grid(True, which="minor", color="grey", linestyle="--")
        ax[0].set_xlim(np.datetime64("2013-06").astype(datetime), max(xs.tolist()))
        ax[0].xaxis.set_major_locator(mdates.YearLocator())
        ax[0].xaxis.set_minor_locator(mdates.MonthLocator())

        ax[1].plot(xs, eff)
        ax[1].plot(xs, ravg_eff)
        ax[1].set_ylabel("Hatékonyság")
        ax[1].set_xlim(np.datetime64("2013-06").astype(datetime), max(xs.tolist()))
        ax[1].xaxis.set_major_locator(mdates.YearLocator())
        ax[1].xaxis.set_minor_locator(mdates.MonthLocator())
        ax[1].grid(True, which="major", color="grey", linestyle="-")
        ax[1].grid(True, which="minor", color="grey", linestyle="--")
        ax[1].set_yticklabels([f"{x:3.0%}" for x in ax[1].get_yticks()])

        plt.tight_layout()
        plt.show()

    def slideplot(self, windowsize=30):
        plt.ion()
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(*self.hun.T, c="black", linewidth=1)
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.grid(True)

        invobj = ax.scatter([], [], c="r", s=30)
        valobj = ax.scatter([], [], c="b", s=5)
        # valobj = self.init_heatmap(ax)
        imidx = 1
        pointstream = self.slide(self.dates.min(), windowsize, 1)
        for xy, ages, iargs, vargs, start in pointstream:
            if not len(xy):
                continue
            self.time_scatter_invalid(xy, ages, iargs, invobj)
            self.time_scatter_valid(xy, ages, vargs, valobj)
            ax.set_title("Hatékonyság: {:.2%}".format(len(iargs) / len(xy)))
            plt.pause(0.01)
            # plt.savefig(f"{projectroot}ImOut/{imidx:0>4}.png", format="png")
            imidx += 1


if __name__ == '__main__':
    plotter = WindowedPlot(filename="olajok.csv")
    plotter.efficiency_curve(windowsize=30)
