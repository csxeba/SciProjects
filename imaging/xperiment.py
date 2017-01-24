import sys
import time
import datetime

from skimage import measure

from csxdata import roots

from SciProjects.imaging import pull_data, preprocess, Results
from SciProjects.imaging.scrape_info import get_mapping
from SciProjects.imaging.algorithm import *

root = "D:/tmp/PIC/"
oldpics = "D:/Dohany_kepanalizis/"
source = "D:/tmp/jpegs/" if sys.platform == "win32" else roots["ntabpics"]
annotpath = "D:/tmp/annotated/"

SCALE = 0.0085812242798
MINAREA = 10000
MINHEIGHT = 1000


def run(randomize=False, verbose=1, **kw):
    outchain = "PIC\tFITPOLY\tFITMXWD\tFITAREA\n"
    pics = pull_data(source=source, randomize=randomize, verbose=verbose)
    mapping = get_mapping(root)
    resultdict = {}

    for i, (pic, path) in enumerate(pics, start=1):
        smplnm, prll = mapping[path[1]]

        lpic = preprocess(pic, dist=False, pictitle=path[1])
        kw["lpic"] = lpic
        # kw["savepath"] = annotpath + path[-1]
        kw["labeltup"] = pic, path

        prps = sorted([prp for prp in measure.regionprops(lpic) if prp.area > MINAREA
                       and prp.image.shape[0] > MINHEIGHT], key=lambda p: p.bbox[0])
        results = algo_fitpolynom(prps, **kw)

        if smplnm not in resultdict:
            resultdict[smplnm] = [[], []]

        resultdict[smplnm][int(prll)-1] = results

    with open("log.txt", "a") as handle:
        handle.write("\n{}\n".format(datetime.datetime.now().strftime("-- %Y.%m.%d_%H.%M.%S")))
        handle.write(outchain)

    names = sorted(resultdict)
    para1 = []
    para2 = []
    for name in names:
        para1 += resultdict[name][0]
        para2 += resultdict[name][1]

    return Results(names, para1, para2)

if __name__ == '__main__':
    start = time.time()
    res = run(show=False, deg=5, SCALE=SCALE, randomize=True)
    print("Run took {:.3f} seconds!".format(time.time()-start))
