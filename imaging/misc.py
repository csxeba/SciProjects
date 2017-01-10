import numpy as np


THRESHOLDS = [1.75, 0.6, 0.6]


def pull_data(source=None):
    from csxdata import roots
    from csxdata.utilities.highlevel import image_sequence_to_array

    source = roots["ntabpics"] if source is None else source
    return image_sequence_to_array(source, outpath=roots["cache"] + "ntabpics.npa", generator=1)


def preprocess(pixels, dist=True):
    # from matplotlib import pyplot as plt
    from scipy import ndimage as ndi
    from skimage import measure

    def binarize(p):
        channel_averages = p.mean(axis=(0, 1)) * THRESHOLDS
        tmp = np.greater_equal(p, channel_averages[None, None, :]).sum(axis=2)
        binned = np.greater_equal(tmp, 3)
        binit = ndi.binary_fill_holes
        nay = np.logical_not
        return nay(binit(nay(binit(binned)), structure=np.ones((3, 3))))

    filled = binarize(pixels)

    # plt.imshow(pixels)
    # plt.show()
    # plt.imshow(filled)
    # plt.show()

    labelled, nlab = measure.label(filled, return_num=True)

    assert nlab > 0

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
