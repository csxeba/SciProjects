from SciProjects.imaging.misc import pull_data, preprocess
from SciProjects.imaging.algorithm import algo_fitpolynom
from skimage import measure

root = "D:/Dohany_kepanalizis/"
annotroot = "D:/tmp/annotated/"
pix = pull_data(root)
results = {}
for pic, (path, flnm) in pix:
    lpic = preprocess(pic, show=False)
    del pic
    results[flnm] = (
        algo_fitpolynom(sorted([prp for prp in measure.regionprops(lpic) if
                                prp.area > 10000 and prp.image.shape[0] > 1000],
                               key=lambda p: p.bbox[0]),
                        deg=5, savepath=annotroot + "annot_" + flnm,
                        labeltup=(path, flnm), lpic=lpic))
