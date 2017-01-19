import sys
import datetime

import numpy as np
import time
from scipy.stats import spearmanr
from scipy import ndimage as ndi
from skimage import measure, feature, morphology
from matplotlib import pyplot as plt

from csxdata import roots

from SciProjects.imaging import pull_data, preprocess


source = "D:/tmp/jpegs/" if sys.platform == "win32" else roots["ntabpics"]

SCALE = 0.0085812242798
MINAREA = 10000
MINHEIGHT = 1000


def algo_fitpolynom(prps, **kw):

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

    def display(lpic):
        picX, picY = lpic.shape
        ax = plt.gca()
        ax.imshow(lpic)
        for i, (prp, log, avg) in enumerate(zip(prps, info, measurements), start=1):
            lcurve, rcurve = log["leftcurve"], log["rightcurve"]
            x0, y0, x1, y1 = prp.bbox
            lsp = np.linspace(1, x1-x0, 100, endpoint=False)
            leftX = lcurve(lsp) + y0
            leftY = lsp + x0
            rightX = rcurve(lsp) + y0
            rightY = lsp + x0
            ax.plot(leftX, leftY, "--", color="yellow")
            ax.plot(rightX, rightY, "--", color="yellow")
            ann = "{}\nleftR:\n{:.4f}\nrightR:\n{:.4f}\nMEAN:\n{:.4f}"\
                .format(i, log["lr"], log["rr"], avg)
            ax.text(y1+10, x1 - 550, ann, color="white")
        ax.set_xlim([0, picY])
        ax.set_ylim([0, picX])
        ax.set_title(labeltup[1])
        plt.show()

    show = kw.get("show", False)
    deg = kw.get("deg", 3)
    labeltup = kw.get("labeltup", "")

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

    if show:
        display(kw["lpic"])

    return measurements


def algo_maxwidth(prps, **kw):

    ridged = ndi.distance_transform_edt(kw["lpic"])

    if kw.get("show", False):
        plt.imshow(ridged)
        plt.show()

    centering = kw.get("centering", np.median)
    slices = (ridged[:, y0:y1] for x0, y0, x1, y1 in (prp.bbox for prp in prps))
    maxes = (centering(slc.max(axis=1)) for slc in slices)
    measurements = [mx * SCALE * 2. for mx in maxes]

    return measurements


def algo_area(prps, **kw):

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


def run(randomize=False, verbose=1, **kw):
    outchain = "PIC\tFITPOLY\tFITMXWD\tFITAREA\n"
    measured = []
    pics = pull_data(source=source, randomize=randomize, verbose=verbose)
    for i, (pic, path) in enumerate(pics, start=1):
        lpic = preprocess(pic, dist=False, pictitle=path[1], show=False)
        kw["lpic"] = lpic
        prps = sorted([prp for prp in measure.regionprops(lpic) if prp.area > MINAREA
                       and prp.image.shape[0] > MINHEIGHT], key=lambda p: p.bbox[0])
        res_fitpoly, res_maxwidth, res_area = [algorithm(prps, **kw) for algorithm in
                                               (algo_fitpolynom, algo_maxwidth, algo_area)]
        results = res_fitpoly, res_maxwidth, res_area
        tuple(map(measured.extend, results))
        lens = tuple(map(len, results))
        assert len(set(lens)) == 1, "poly: {} mxwd: {} area: {}".format(*lens)
        for j in range(len(res_fitpoly)):
            samplename = "{}-{}".format(path[1], j)
            outchain += "{}\t{}\t{}\t{}\n".format(
                samplename, res_fitpoly[j], res_maxwidth[j], res_area[j])

    print("Measurements:")
    print("\n".join(str(m) for m in measured))

    glob = np.median(measured)
    print("Global median: in mms: {}".format(glob))
    print("Total number of objects inspected: {}".format(len(measured)))

    with open("log.txt", "a") as handle:
        handle.write("\n{}\n".format(datetime.datetime.now().strftime("-- %Y.%m.%d_%H.%M.%S")))
        handle.write(outchain)
        handle.write("GLOBAL MEDIAN: {}\n".format(glob))

    return measured

if __name__ == '__main__':
    start = time.time()
    run(show=False, deg=9)
    print("Run took {:.3f} seconds!".format(time.time()-start))
