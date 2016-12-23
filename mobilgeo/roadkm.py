import numpy as np

from shapefile import Reader
from Project_MobileGeo.utility import haversine, euclidean, sort_coords

# Header of shapefile records:
# ('DeletionFlag', 'C', 1, 0)
# ['UT_SZAM', 'C', 5, 0]
# ['KATEGORIA', 'C', 20, 0]

BUDAPEST = np.array([19.040833, 47.498333])[None, ...]

projectroot = "D:/Project_MobilGeo/"
shproot = "E:/tmp/"


def pull_data():
    roads = Reader(shproot + "roads_wgs.shp")
    print("HEADER:", "\n".join(str(f) for f in roads.fields), sep="\n")
    shaperecs = roads.shapeRecords()

    with open(projectroot + "foutkm.csv") as infl:
        lines = [line.split("\t") for line in infl]

    return shaperecs


def get_road_coords(no_road, shaperecs, sort=True):

    def get_candidate():
        candidates = [shr for shr in shaperecs if shr.record[0] == str(no_road)]
        if not candidates:
            return None
        candidates.sort(key=lambda shr: len(shr.shape.points), reverse=True)
        return candidates[0]

    def determine_arg_of_starting_point_coordinate(coords):
        d = euclidean(coords, BUDAPEST)
        arg = d.argmin()
        return arg

    candidate = get_candidate()
    if not candidate:
        print("!! No such road:", no_road)
        return None
    points = np.array(list(set(candidate.shape.points)))
    if sort:
        road_start = determine_arg_of_starting_point_coordinate(points)
        return sort_coords(points, start_index=road_start)
    return points


def cumulative_length(points, metrics):
    d = 0
    for left, right in zip(points[:-1], points[1:]):
        distance = metrics(left, right)
        d += distance
    return d


def interplolate_coordinates(travelled, no_road):
    coords = get_road_coords(no_road, geodata, sort=True)
    distance = 0
    left = right = None
    for left, right in zip(coords[:-1], coords[1:]):
        d = haversine(left, right)
        if distance + d >= travelled:
            break
        distance += d
    return left + right / 2.


def scatter(points):
    from matplotlib import pyplot as plt
    ax = plt.axes()
    asarr = np.array(points)
    for (sx, sy), (ex, ey) in zip(points[:-1], points[1:]):
        dx = ex-sx
        dy = ey-sy
        ax.arrow(sx, sy, dx, dy, width=0.0001, length_includes_head=True,
                 head_width=0.0003)
    plt.xlim(asarr[:, 0].min(), asarr[:, 0].max())
    plt.ylim(asarr[:, 1].min(), asarr[:, 1].max())
    plt.show()


def dump_coords(points, ID=""):
    outpath = "E:/tmp/Coordinates{}.csv".format(ID)
    chain = "ID\tX\tY\n"
    chain += "\n".join(str(i) + "\t" + "\t".join(str(e) for e in line) for i, line in enumerate(points))
    handle = open(outpath, "w")
    handle.write(chain)
    handle.close()
    print("Dumped coords to", outpath)


if __name__ == '__main__':
    geodata = pull_data()
    print("45th km stone of road 4:", interplolate_coordinates(45, 4))
