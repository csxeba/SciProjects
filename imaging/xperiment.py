import numpy as np
from skimage import measure, feature
from matplotlib import pyplot as plt

from SciProjects.imaging import pull_data, preprocess, pprint

source = "D:/tmp/jpegs/"
pics = pull_data(source=source, randomize=True, verbose=1)

# R-G-B
MAX_LBLS = 3
# picX, picY, picZ = 1944, 2592, 3
MAXFSIZE = 50
SCALE = 0.0085812242798
UPSCALE = 2.
verbose = 1
MINAREA = 10000


def algo_fitpolynom(dpic, lpic, nlab, **kw):

    show = kw.get("show", False)

    picX, picY = lpic.shape
    prps = [prp for prp in measure.regionprops(lpic)
            if prp.area > MINAREA or prp.image.shape[0] > 1000]
    measurements = []
    curves = []
    for prp in prps:
        x0, y0, x1, y1 = prp.bbox
        edge = np.argwhere(feature.canny(prp.image))
        leftedge, rightedge = [], []
        la, ra = leftedge.append, rightedge.append
        for y in range(y1):
            ft = [e[1] for e in edge if e[0] == y]
            if len(ft) == 0:
                continue
            la((y, min(ft)))
            ra((y, max(ft)))

        leftedge, rightedge = np.array(leftedge).T, np.array(rightedge).T
        lefts = []
        rights = []
        for i in range(3, 7):
            leftcurve, lr, _, _, _ = np.polyfit(*leftedge, deg=i, full=True)
            rightcurve, rr, _, _, _ = np.polyfit(*rightedge, deg=i, full=True)
            lefts.append((leftcurve, lr, i))
            rights.append((rightcurve, rr, i))
        lefts.sort(key=lambda tup: tup[1])
        rights.sort(key=lambda tup: tup[1])
        leftcurve, lr, dl = lefts[0]
        rightcurve, rr, dr = rights[0]
        leftcurve, rightcurve = np.poly1d(leftcurve), np.poly1d(rightcurve)
        curves.append((leftcurve, rightcurve))

        print("left R: {}, deg: {}\nright R: {}, deg: {}".format(lr, dl, rr, dr))

        lefti = leftcurve.integ()
        righti = rightcurve.integ()

        # S <x0, x1> f(x) dx - S <x0, x1> g(x) dx
        # ---------------------------------------
        #                x1 - x0
        avgdistance = ((righti(y1) - righti(y0)) - (lefti(y1) - lefti(y0))) / (y1 - y0)
        measurements.append(avgdistance * SCALE)

    if show:
        plt.imshow(lpic)
        lsp = np.linspace(0, picY, 200)
        for prp, (leftcurve, rightcurve) in zip(prps, curves):
            x0, y0, x1, y1 = prp.bbox
            leftX = leftcurve(lsp) + y0
            leftY = lsp + x0
            rightX = rightcurve(lsp) + y0
            rightY = lsp + x0
            plt.plot(leftX, leftY, "--", color="yellow")
            plt.plot(rightX, rightY, "--", color="yellow")
        axes = plt.gca()
        axes.set_xlim([0, picY])
        axes.set_ylim([0, picX])
        plt.show()
    return measurements


def algo_maxwidth(dpic, lpic, nlab, **kw):
    show = kw.get("show", 0)
    centering = kw.get("centering", np.mean)
    if show:
        plt.imshow(dpic)
        plt.show()
        if show > 1:
            plt.imshow(lpic)
            plt.show()

    bboxes = (prp.bbox for prp in measure.regionprops(lpic) if prp.area > MINAREA)
    slices = (dpic[:, y0:y1] for x0, y0, x1, y1 in bboxes)
    maxes = (centering(slc.max(axis=1)) for slc in slices)
    measurements = [mx * SCALE * UPSCALE for mx in maxes]

    if len(measurements) < nlab:
        pprint("Skipped {} particles due to suspiciously small area!"
               .format(nlab - len(measurements)))

    return measurements


# noinspection PyUnusedLocal
def algo_area(dpic, lpic, nlab, **kw):

    show = kw.get("show", False)

    def display():
        nosp = len(prps) + (0 if len(prps) % 2 == 0 else 1)
        fig, axes = plt.subplots(2, nosp // 2)
        axes = axes.ravel()
        for i, prp in enumerate(prps):
            axes[i].imshow(prp.image)
        plt.show()

    prps = [prp for prp in measure.regionprops(lpic) if prp.area > MINAREA and prp.image.shape[0] > 1000]
    bboxes = (prp.bbox for prp in prps)
    measurements = [(prp.area / (x1-x0)) * SCALE for
                    prp, (x0, y0, x1, y1) in zip(prps, bboxes)]
    if show:
        display()

    if len(measurements) < nlab:
        print("Skipped {} props with area < 10000".format(nlab - len(measurements)))

    return measurements


def run(algorithm, **kw):
    measured = []
    for i, (dpic, lpic, nlab) in enumerate(map(preprocess, pics), start=1):
        means = algorithm(dpic, lpic, nlab, **kw)
        print("\n".join(str(round(m, 3)) for m in means))
        measured.extend(means)

    pprint("Measurements:")
    pprint("\n".join(str(m) for m in measured))

    glob = sum(measured) / len(measured)
    pprint("Global median: in pxls: {}".format(glob))
    pprint("               in mms : {} mm".format(glob))
    pprint("Total number of objects inspected: {}".format(len(measured)))
    return measured

if __name__ == '__main__':
    run(algo_fitpolynom, show=True)
