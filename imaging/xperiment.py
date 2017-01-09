import warnings

import numpy as np
from scipy import ndimage as ndi
from matplotlib import pyplot as plt
from skimage import measure

from SciProjects.imaging import pull_data

pics = pull_data()

# R-G-B
THRESHOLDS = [1.75, 0.6, 0.6]
MAX_LBLS = 3
picX, picY, picZ = 1944, 2592, 3
MAXFSIZE = 50
SCALE = 0.00858122427983539094650205761317
UPSCALE = 2.
NOMEASUREMENTS = 5


def preprocess(pixels):

    def binarize(p):
        channel_averages = p.mean(axis=(0, 1)) * THRESHOLDS
        tmp = np.greater_equal(p, channel_averages[None, None, :]).sum(axis=2)
        binned = np.greater_equal(tmp, 3)
        binit = ndi.binary_fill_holes
        nay = np.logical_not
        return nay(binit(nay(binit(binned)), structure=np.ones((3, 3))))

    filled = binarize(pixels)
    labelled, nlab = measure.label(filled, return_num=True)

    assert nlab > 0

    # assert nlab <= MAX_LBLS, "NO labelled objects exceed set limit! ({} > {})".format(nlab, MAX_LBLS)

    ridged = ndi.distance_transform_edt(filled)

    return ridged, labelled, nlab


def from_maxwidths(dpic, lpic, nlab):
    bboxes = [prp.bbox for prp in measure.regionprops(lpic)]
    measurements = []
    for x0, y0, x1, y1 in bboxes:
        if x0 != 0.0 or x1 != picX:
            print("Skipped particle @ x: {}, y: {}".format((x0, x1), (y0, y1)))
            continue

        eighths = np.array([x1 // 8] * 5) * np.arange(2, 2+5)

        sliced = dpic[:, y0:y1]
        maxes = sliced.max(axis=1)[eighths]
        measurements.append(maxes.mean() * UPSCALE)
        # sliced[eighths] += 1000.
        # plt.matshow(sliced)
        # plt.show()

    if len(measurements) < nlab:
        warnings.warn("Skipped {} particles due to suspiciously small size!"
                      .format(nlab - len(measurements)))

    return measurements


def from_area(dpic, lpic, nlab):
    measurements = []
    for prop in measure.regionprops(lpic):
        x0, y0, x1, y1 = prop.bbox
        if x0 != 0.0 or x1 != picX:
            print("Skipped particle @ x: {}, y: {}".format((x0, x1), (y0, y1)))
            continue
        measurements.append(prop.area / picX)
    return measurements


def main():
    print("Self-assertions:")
    print("Image height: {} mm".format(picX * SCALE))
    measured = []
    for i, (dpic, lpic, nlab) in enumerate(map(preprocess, pics), start=1):
        print("Doing pic {0:>{w}}/{1}".format(i, 14, w=2))
        assert dpic.shape == (picX, picY), ("Invalid input picture dimensions!\n{} != {}"
                                            .format(dpic.shape, (picX, picY)))

        means = from_maxwidths(dpic, lpic, nlab)
        measured.extend(means)

    print("Measurements:")
    print("\n".join(str(m * SCALE) for m in measured))

    glob = sum(measured) / len(measured)
    print("Global average: in pxls: {}".format(glob))
    print("                in mms : {} mm".format(glob*SCALE))
    print("Total number of objects inspected: {}".format(len(measured)))

if __name__ == '__main__':
    main()
