from skimage import io, measure


def get_image(path):
    flnm = path.split("/")[-1]
    dirz = "/".join(path.split("/")[:-1])
    binned = (io.imread(path) / 255).astype(bool)
    labelled = measure.label(binned)
    prps = measure.regionprops(labelled)
    return prps, flnm, dirz
