import numpy as np
from matplotlib import pyplot as plt
from shapefile import Reader

from csxdata import roots
from csxdata.utilities.vectorops import split_by_categories, featscale, downscale

from SciProjects.riskanalyze import projectroot
from SciProjects.riskanalyze.utils import pull_data

# data header: RENDSZAM	SZOLGHELY	DATUM	HELY	MINTA	MEGF


def _time_scatter(xy, args, mpl_obj):
    if len(args) < 0:
        return 0
    mpl_obj.set_offsets(xy[args])
    return 1


class WindowedPlot:

    xy, data = pull_data()
    dates, valid = data[:, 2], data[:, 5]
    dates = np.array([s.replace(".", "-") for s in dates], dtype="datetime64[D]")
    hun = np.array(Reader(roots["gis"] + "hun/HUN_adm0.shp").shapes()[0].points)
    rhun, _dfctr, _ufctr = featscale(hun, return_factors=True)
    rxy = downscale(xy, *_dfctr)
    fig, ax = plt.subplots()

    @property
    def sxy(self):
        return split_by_categories(self.valid, self.xy)

    def select(self, begin, end,):
        mask = np.logical_and(self.dates >= begin, self.dates <= end)
        return self.rxy[mask], self.dates[mask], self.valid[mask]

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

    def time_scatter_valid(self, xy, ages, args, mpl_obj):
        if not _time_scatter(xy, args, mpl_obj):
            return
        szs = (1.5 * (ages[args]+1))**5
        mpl_obj.set_sizes(szs)

    def time_scatter_invalid(self, xy, ages, args, mpl_obj):
        if not _time_scatter(xy, args, mpl_obj):
            return
        # mpl_obj.set_sizes(10 * (ages[args]+1))

    def init_heatmap(self):
        hm, xe, ye = np.histogram2d(self.rxy[:, 0], self.rxy[:, 1], bins=100)
        hm /= hm.max()
        obj = self.ax.imshow(hm, extent=(xe[0], xe[-1], ye[0], ye[-1]),
                             vmin=0, vmax=1)
        return obj

    def heatmap_valid(self, xy, ages, args, mpl_obj):
        # w = (1.5 * ages[args]+1) ** 4  # type: np.ndarray
        hm, xe, ye = np.histogram2d(xy[args, 0], xy[args, 1], bins=100)
        mpl_obj.set_data(hm)

    def slideplot(self):
        plt.ion()
        self.ax.plot(*self.rhun.T, c="black", linewidth=1)
        self.ax.set_xlim([0, 1]); self.ax.set_ylim([0, 1]); self.ax.grid(True)

        invobj = self.ax.scatter([], [], c="r", s=30)
        valobj = self.ax.scatter([], [], c="b", s=5)
        # valobj = self.init_heatmap()
        start = self.dates.min()
        stepsize = np.timedelta64(30)
        imidx = 1
        while start + stepsize < self.dates.max():
            # print("Displaying", start, "-", start+stepsize*2)
            xy, ages, iargs, vargs = self.get_current_points(start, start+stepsize)
            if not len(xy):
                start += 2
                continue
            self.time_scatter_invalid(xy, ages, vargs, valobj)
            self.time_scatter_valid(xy, ages, iargs, invobj)
            start += 2
            self.ax.set_title("{} -- {}".format(start, start + stepsize))
            plt.pause(0.01)
            plt.savefig(f"{projectroot}ImOut/{imidx:0>4}.png", format="png")
            imidx += 1


if __name__ == '__main__':
    plotter = WindowedPlot()
    plotter.slideplot()
