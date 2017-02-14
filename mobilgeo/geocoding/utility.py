import math

import numpy as np

R = 6379743.001
Lambda0 = .33246029531
e = .0818205679407
k = 1.003110007693
n = 1.000719704936
m0 = 0.99993
fi0 = 0.822050077


def euclidean(coords1, coords2):
    return np.linalg.norm(coords2 - coords1, axis=1)


def haversine(coords1, coords2):
    lat1, lon1 = coords1
    lat2, lon2 = coords2
    dlon = math.radians(lon2 - lon1)
    dlat = math.radians(lat2 - lat1)
    lat1, lat2 = [math.radians(l) for l in (lat1, lat2)]

    a = math.sin(dlat/2.)**2. + math.cos(lat1)*math.cos(lat2)*(math.sin(dlon/2.)**2.)
    c = 2. * math.asin(math.sqrt(a))
    return c * R


def wgs_to_eov(coords):
    """
    Source:
    http://www.agt.bme.hu/staff_h/zaletnyik/TDK_EOV.pdf
    """
    lon, lat = coords
    part1 = math.pi / 4. + lon / 2.
    part2 = ((1. - e*math.sin(lon)) / (1. + e*math.sin(lon))) ** (n * e * 0.5)
    part3 = k * (math.tan(part1 * part2) ** n) - (math.pi / 4.)
    nlon = 2*part3
    nlat = n * (lat - Lambda0)
    return nlon, nlat


def eov_to_wgs(coords):
    """
    Source:
    http://www.agt.bme.hu/staff_h/zaletnyik/TDK_EOV.pdf
    """
    lon, lat = coords
    x, y = lat-200000., lon-650000.
    part1 = e ** (x / (R * m0))
    part_lat = 2. * math.atan(part1) - (math.pi - 2.)
    part_lon = y / (R * m0)

    part2 = math.sin(part_lon) * math.cos(fi0)
    part3 = math.sin(fi0) * math.cos(part_lon) * math.cos(part_lat)
    part_lon = math.asin(part2 + part3)

    part4 = math.cos(part_lon) * math.sin(part_lat)
    part_lat = math.asin(part4 / math.cos(part_lon))

    nlat = Lambda0 + part_lat / n

    part5 = math.tan(math.pi / 4. + part_lon / 2.) / k
    nlon = 2. * math.atan(part5 ** (1. / n)) - math.pi / 2.

    for i in range(100):
        part6 = math.tan(math.pi / 4. + nlon / 2.)
        part7a = (1. - e * math.sin(nlon))
        part7b = (1. + e * math.sin(nlon))
        part7 = (part7a / part7b)
        part8 = k * part7 ** (n*e*0.5)
        part9 = (part6 / part8) ** (1. / n)
        nlon = 2. * math.atan(part9) - math.pi / 2.

    return nlon, nlat


def argsort_coords(coords, start_index):
    """Nearest-neighbour sorting given the starting point"""
    from scipy.spatial.distance import pdist, squareform
    output = [start_index]
    D = squareform(pdist(coords))
    arg = start_index
    while len(output) != coords.shape[0]:
        sort = D[arg].argsort()
        arg = sort[1]
        i = 0
        while arg in output:
            arg = sort[i + 1]
            i += 1
        output.append(arg)
    return output


def sort_coords(coords, start_index):
    args = argsort_coords(coords, start_index)
    return coords[args]
