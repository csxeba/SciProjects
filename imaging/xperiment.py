import numpy as np
from skimage import measure
from matplotlib import pyplot as plt

from SciProjects.imaging import pull_data, preprocess, pprint


pics = pull_data()

# R-G-B
MAX_LBLS = 3
# picX, picY, picZ = 1944, 2592, 3
MAXFSIZE = 50
SCALE = 0.00858122427983539094650205761317
UPSCALE = 2.
verbose = 1
MINAREA = 10000


def algo_maxwidth(dpic, lpic, nlab, centerwith, show=0):
    if show:
        plt.imshow(dpic)
        plt.show()
        if show > 1:
            plt.imshow(lpic)
            plt.show()

    bboxes = (prp.bbox for prp in measure.regionprops(lpic) if prp.area > MINAREA)
    slices = (dpic[:, y0:y1] for x0, y0, x1, y1 in bboxes)
    maxes = (centerwith(slc.max(axis=1)) for slc in slices)
    measurements = [mx * SCALE * UPSCALE for mx in maxes]

    if len(measurements) < nlab:
        pprint("Skipped {} particles due to suspiciously small area!"
               .format(nlab - len(measurements)))

    return measurements


# noinspection PyUnusedLocal
def algo_area(dpic, lpic, nlab, centering=None, show=0):
    if show:
        plt.imshow(lpic)
        plt.show()

    prps = measure.regionprops(lpic)
    bboxes = (prp.bbox for prp in prps)
    measurements = [(prp.area / (x1-x0)) * SCALE for prp, (x0, y0, x1, y1) in
                    zip(prps, bboxes) if prp.area > MINAREA]

    if len(measurements) < nlab:
        print("Skipped {} props with area < 10000".format(nlab - len(measurements)))

    return measurements


def run(algorithm, **kw):
    import os
    from csxdata import roots
    nopics = len([fl for fl in os.listdir(roots["ntabpics"])])

    measured = []
    for i, (dpic, lpic, nlab) in enumerate(map(preprocess, pics), start=1):
        pprint("Doing pic {0:>{w}}/{1} ".format(i, nopics, w=len(str(nopics))))
        means = algorithm(dpic, lpic, nlab, kw.get("centering", np.mean), 1)
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
    run(algo_maxwidth)
