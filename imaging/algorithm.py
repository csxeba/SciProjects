"""
Copyright (C) 2017 Csaba Gór
gor.csaba@nav.gov.hu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np
from scipy import ndimage as ndi
from scipy.stats import spearmanr
from skimage import feature, morphology
from matplotlib import pyplot as plt


def algo_fitpolynom(prps, **kw):

    SCALE = kw.get("SCALE", 0.0085812242798)
    savepath = kw.get("savepath", None)
    show = kw.get("show", False)
    deg = kw.get("deg", 3)
    labeltup = kw.get("labeltup", "")

    def extrac_prop_edges(prop, height):
        y = np.arange(height)
        edge = feature.canny(prop.image)
        selem = np.zeros((3, 3))
        selem[:, 1] = 1
        edge = morphology.binary_dilation(edge, selem=selem)
        left = height - np.max(edge[:, ::-1] * y, axis=1)
        lx = np.argwhere(np.not_equal(left, height)).ravel()
        left = np.stack((lx, left[lx]))
        right = np.max(edge * y, axis=1)
        rx = np.argwhere(np.greater(right, 0)).ravel()
        right = np.stack((rx, right[rx]))
        return left, right, lx, rx

    def fit_polynoms_to_edges(left, right, degree):
        lpoly = np.polyfit(*left, deg=degree)
        rpoly = np.polyfit(*right, deg=degree)
        lcurve, rcurve = np.poly1d(lpoly), np.poly1d(rpoly)
        l_rsq = spearmanr(leftedge[1], lcurve(leftedge[0]))[0] ** 2
        r_rsq = spearmanr(rightedge[1], rcurve(rightedge[0]))[0] ** 2
        return lcurve, rcurve, l_rsq, r_rsq

    def integrate_and_calculate_width_cut(lcurve, rcurve, lx, rx):
        # S <x0, x1> f(x) dx - S <x0, x1> g(x) dx
        # ---------------------------------------
        #                x1 - x0
        ix0, ix1 = max(lx[0], rx[0]), min(lx[-1], rx[-1])
        idx = ix1 - ix0
        li = lcurve.integ()
        ri = rcurve.integ()
        wcut = ((ri(ix1) - ri(ix0)) - (li(ix1) - li(ix0))) / idx
        return wcut

    def build_pic(lpic):
        picX, picY = lpic.shape
        fig = plt.figure()
        ax = fig.gca()
        ax.imshow(lpic)
        for i, (prp, log, avg) in enumerate(zip(prps, info, measurements), start=1):
            lcurve, rcurve = log["leftcurve"], log["rightcurve"]
            x0, y0, x1, y1 = prp.bbox
            lsp = np.linspace(1, x1-x0, 100, endpoint=False)
            leftX = lcurve(lsp) + y0
            leftY = lsp + x0
            rightX = rcurve(lsp) + y0
            rightY = lsp + x0
            _time_scatter(leftX, leftY, "--", color="yellow")
            _time_scatter(rightX, rightY, "--", color="yellow")
            ann = "{}\nleftR:\n{:.4f}\nrightR:\n{:.4f}\nMEAN:\n{:.4f}"\
                .format(i, log["lr"], log["rr"], avg)
            ax.text(y1+10, x1 - 650, ann, color="white")
        ax.set_xlim([0, picY])
        ax.set_ylim([0, picX])
        ax.set_title(labeltup[1])
        if savepath is not None:
            try:
                fig.savefig(savepath)
            except MemoryError:
                print("Failed to save to {}".format(savepath))
        if show:
            plt.show()
        plt.close()

    measurements = []
    info = []
    for prp in prps:
        dx, dy = prp.image.shape

        leftedge, rightedge, leftx, rightx = extrac_prop_edges(prp, dy)
        leftcurve, rightcurve, lr, rr = fit_polynoms_to_edges(leftedge, rightedge, deg)
        avgdistance = integrate_and_calculate_width_cut(leftcurve, rightcurve, leftx, rightx)
        measurements.append(avgdistance * SCALE)

        inf = {"leftcurve": leftcurve, "lr": lr,
               "rightcurve": rightcurve, "rr": rr}
        info.append(inf)

    if show or savepath:
        build_pic(kw["lpic"])

    return measurements


def algo_maxwidth(prps, **kw):

    SCALE = kw.get("SCALE", 0.0085812242798)
    show = kw.get("show", False)

    ridged = ndi.distance_transform_edt(kw["lpic"])

    if show:
        plt.imshow(ridged)
        plt.show()

    centering = kw.get("centering", np.median)
    slices = (ridged[:, y0:y1] for x0, y0, x1, y1 in (prp.bbox for prp in prps))
    maxes = (centering(slc.max(axis=1)) for slc in slices)
    measurements = [mx * SCALE * 2. for mx in maxes]

    return measurements


def algo_area(prps, **kw):

    SCALE = kw.get("SCALE", 0.0085812242798)
    show = kw.get("show", False)

    def display():
        nosp = len(prps) + (0 if len(prps) % 2 == 0 else 1)
        fig, axes = plt.subplots(2, nosp // 2)
        axes = axes.ravel()
        for i, prp in enumerate(prps):
            axes[i].imshow(prp.image)
        plt.show()

    dxes = (x1-x0 for x0, y0, x1, y1 in (prp.bbox for prp in prps))
    measurements = [(prp.area / dx) * SCALE for prp, dx in zip(prps, dxes)]
    if show:
        display()

    return measurements


algorithms = [algo_fitpolynom, algo_maxwidth, algo_area]
