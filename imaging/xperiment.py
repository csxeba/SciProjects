import time

from skimage import measure

from SciProjects.imaging import pull_data, preprocess
from SciProjects.imaging.scrape_info import get_mapping
from SciProjects.imaging.algorithm import *

root = "/home/csa/tmp/PIC/"
oldpics = "/home/csa/Dohany_kepanalizis/"
source = "/home/csa/tmp/jpegs/"
annotpath = "/home/csa/tmp/annotated/"

SCALE = 0.0085812242798
MINAREA = 10000
MINHEIGHT = 1000


def run(randomize=False, verbose=1, **kw):
    outchain = "PIC\tSMPL\tRPLC\tPRP\tFITPOLY\tFITMXWD\tFITAREA\n"
    pics = pull_data(source=source, randomize=randomize, verbose=verbose)
    mapping = get_mapping(root)
    saveroot = kw.get("savepath", "")

    for i, (pic, path) in enumerate(pics, start=1):
        assert len(path) == 2, "Died: path: {}".format(path)
        smplnm, prll = mapping[path[1]]

        lpic = preprocess(pic, dist=False, pictitle=path[1])
        kw["lpic"] = lpic
        # kw["savepath"] = annotpath + path[-1]
        kw["labeltup"] = pic, path
        if "savepath" in kw:
            kw["savepath"] = saveroot + "annot_" + path[1] + ".png"

        prps = sorted([prp for prp in measure.regionprops(lpic) if prp.area > MINAREA
                       and prp.image.shape[0] > MINHEIGHT], key=lambda p: p.bbox[0])

        results = np.array([algo(prps, **kw) for algo in algorithms])

        assert results.ndim == 2

        for j, res in enumerate(results.T, start=1):
            outchain += "\t".join((path[1], smplnm + "_", prll, str(i))) + "\t"
            outchain += "\t".join(res.astype(str)).replace(".", ",")
            outchain += "\n"

    with open("log.txt", "w") as handle:
        # handle.write("\n{}\n".format(datetime.datetime.now().strftime("-- %Y.%m.%d_%H.%M.%S")))
        handle.write(outchain)

if __name__ == '__main__':
    start = time.time()
    run(show=False, deg=5, SCALE=SCALE, randomize=True, savepath="/home/csa/tmp/annotated/")
    print("Run took {:.3f} seconds!".format(time.time()-start))
