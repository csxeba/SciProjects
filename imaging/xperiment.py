import sys
import time
import datetime

from skimage import measure

from csxdata import roots

from SciProjects.imaging import pull_data, preprocess
from SciProjects.imaging.algorithm import *


oldpics = "D:/Dohany_kepanalizis/"
source = "D:/tmp/jpegs/" if sys.platform == "win32" else roots["ntabpics"]
annotpath = "D:/tmp/annotated/"

SCALE = 0.0085812242798
MINAREA = 10000
MINHEIGHT = 1000


def run(randomize=False, verbose=1, **kw):
    outchain = "PIC\tFITPOLY\tFITMXWD\tFITAREA\n"
    measured = [[], [], []]
    pics = pull_data(source=oldpics, randomize=randomize, verbose=verbose)

    for i, (pic, path) in enumerate(pics, start=1):
        lpic = preprocess(pic, dist=False, pictitle=path[1], show=True)
        kw["lpic"] = lpic
        # kw["savepath"] = annotpath + path[-1]
        kw["labeltup"] = pic, path

        prps = sorted([prp for prp in measure.regionprops(lpic) if prp.area > MINAREA
                       and prp.image.shape[0] > MINHEIGHT], key=lambda p: p.bbox[0])
        results = [alg(prps, **kw) for alg in algorithms]
        for m, r in zip(measured, results):
            m.extend(r)

        lens = tuple(map(len, results))
        assert len(set(lens)) == 1, "poly: {} mxwd: {} area: {}".format(*lens)

        for j in range(len(results[0])):
            samplename = "{}-{}".format(path[1], j)
            outchain += "{}\t{}\t{}\t{}\n".format(
                samplename, results[0][j], results[1][j], results[2][j])

    glob = np.median(measured)
    print("Global median: in mms: {}".format(glob))
    print("Total number of objects inspected: {}".format(len(measured[0])))

    with open("log.txt", "a") as handle:
        handle.write("\n{}\n".format(datetime.datetime.now().strftime("-- %Y.%m.%d_%H.%M.%S")))
        handle.write(outchain)
        handle.write("GLOBAL MEDIAN: {}\n".format(glob))

    return measured

if __name__ == '__main__':
    start = time.time()
    run(show=False, deg=5, SCALE=SCALE, randomize=True)
    print("Run took {:.3f} seconds!".format(time.time()-start))
