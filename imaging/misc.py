import os

import numpy as np
from skimage import exposure, filters, measure, feature

# NOT USED ATM
THRESHOLDS = [1., 2., 0.]


def pull_data(source=None, randomize=False, verbose=0):
    from csxdata import roots
    from csxdata.utilities.highlevel import image_to_array

    source = roots["ntabpics"] if source is None else source
    pics = np.array([source + fl for fl in os.listdir(source)])
    if randomize:
        np.random.shuffle(pics)
    for i, path in enumerate(pics, start=1):
        if verbose:
            print("PIC {:>{w}}/{}".format(i, len(path), w=len(str(len(path)))))
        yield image_to_array(path)


def preprocess(pixels, dist=True, show=True):
    from scipy import ndimage as ndi
    from matplotlib import pyplot as plt

    binit = ndi.binary_fill_holes
    nay = np.logical_not

    def equalize(p):
        return exposure.equalize_adapthist(p[:, :, 0])

    def binarize_by_hardcoded_thresholding(p):
        # thresh = p.mean(axis=(0, 1)) * THRESHOLDS
        thresh = np.array([80, 120, 256])
        tmp = np.greater_equal(p, thresh[None, None, :]).sum(axis=2)
        binned = np.greater_equal(tmp, 1)
        return nay(binit(nay(binit(binned)), structure=np.ones((5, 5))))

    def binarize_by_mean_thresholding(p):
        thresh = p.mean(axis=(0, 1)) * THRESHOLDS
        tmp = np.greater_equal(p, thresh[None, None, :]).sum(axis=2)
        binned = np.greater_equal(tmp, 1)
        return nay(binit(nay(binit(binned)), structure=np.ones((5, 5))))

    def binarize_by_otsu_threasholding(p):
        thresh = filters.threshold_otsu(p)
        tmp = np.greater_equal(p, thresh)
        return nay(binit(nay(binit(tmp))))

    def binarize_by_edge_detection(p):
        edges = sum((feature.canny(p[:, :, i] / 255.) for i in range(2)))
        binned = np.greater_equal(edges, 2)
        plt.imshow(binned)
        plt.show()
        return nay(binit(nay(binit(binned)), structure=np.ones((3, 3))))

    eqd = equalize(pixels)
    filled = binarize_by_otsu_threasholding(eqd)

    labelled, nlab = measure.label(filled, return_num=True)

    if show:
        fig, axes = plt.subplots(2, 2)
        axes = axes.ravel()
        for i, im in enumerate((pixels, eqd, filled, labelled)):
            axes[i].imshow(im)
        plt.show()

    if not dist:
        return labelled, nlab

    ridged = ndi.distance_transform_edt(filled)
    return ridged, labelled, nlab


def pprint(*args, **kw):
    vb = globals().get("verbose", None)
    vb = kw.get("verbose", None) if vb is None else vb
    if vb in (False, 0):
        return
    kw = {k: v for k, v in kw.items() if k != "verbose"}
    print(*args, **kw)
