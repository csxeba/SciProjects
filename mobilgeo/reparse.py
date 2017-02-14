import numpy as np

from csxdata.utilities.vectorops import argfilter
from SciProjects.mobilgeo.geocoding.placetypes import *


def fix_carno(carno: str):
    return carno.replace(" ", "").replace("-", "")


def fix_address(chain):
    return chain\
        .replace(",", " ")\
        .replace(".", " ")

fix_carno = np.vectorize(fix_carno)
fix_address = np.vectorize(fix_address)


def read(path):
    chain = open(path, encoding="utf-8-sig").read()
    # chain = dehungarize(chain)
    lines = chain.split("\n")
    head = lines.pop(0).split("\t")
    matrix = np.array([line.split("\t") for line in lines if line])
    return matrix, head


def reparse_data(outflpath):
    data, dheader = read("/home/csa/Project_MobilGeo/AdatSum_olaj.csv")
    data[:, 0] = fix_carno(data[:, 0])
    data[:, 4] = np.vectorize(str.lower)(data[:, 4])
    args = np.concatenate((
        argfilter(data[:, 4], "gázolaj"),
        argfilter(data[:, 4], "benzin")))
    data = data[args][:, 0, :]
    with open(outflpath, "w") as handle:
        handle.write("\t".join(dheader) + "\n")
        handle.write("\n".join("\t".join(line) for line in data))
        handle.close()


def extract_unique_placenames():
    data, head = read("/home/csa/Project_MobilGeo/AdatSum_olaj.csv")
    placenames = np.array(list(set(data[:, 3])))
    print("Found", len(placenames), "unique placenames")
    with open("/home/csa/Project_MobilGeo/Helyek.csv", "w") as handle:
        handle.write("\n".join(pn for pn in placenames if pn))


def geocode_placenames():
    root = "/home/csa/Project_MobilGeo/cimek/"
    kt = sorted(list(set([ln.strip() for ln in open(root + "ktbt.csv")])))
    hr = sorted(list(set([ln.strip() for ln in open(root + "hrsz.csv")])))
    nc = sorted(list(set([ln.strip() for ln in open(root + "nice.csv")])))

    objects = []
    input("DOING HRSZ! ({})".format(len(hr)))
    objects += [HRSZ(hrsz) for hrsz in hr]
    input("DOING NiceAddress! ({})".format(len(nc)))
    objects += [NiceAddress(nice) for nice in nc]
    input("DOING KTBT! ({})".format(len(kt)))
    objects += [KTBT(ktbt) for ktbt in kt]

    handle = open(root + "geocoded.csv", "r")
    addresses = [line[-1] for line in handle]
    handle.close()
    handle = open(root + "geocoded.csv", "a")
    handle.write("RAW\tADDR\tX\tY\tFOUND\n")
    for i, obj in enumerate(objects, start=1):
        print(f"\rDoing {i:>4}/{len(objects)}", end="")
        if obj.found in addresses:
            continue
        obj.geocode()
        addresses.append(obj.found)
        handle.write(obj.to_outputline())
    print()


def match_coords():
    data, dheader = read("/home/csa/Project_MobilGeo/AdatSum_olaj.csv")
    data[:, 0] = fix_carno(data[:, 0])
    data[:, 4] = np.vectorize(str.lower)(data[:, 4])
    args = np.concatenate((
        argfilter(data[:, 4], "gazolaj"),
        argfilter(data[:, 4], "benzin")))
    data = data[args][:, 0, :]

    coords, cheader = read("/home/csa/Project_MobilGeo/Kimenet.csv")
    coords[:, 0] = np.vectorize(lambda string: string[len("Hungary, "):])(coords[:, 0])

    data[:, 3] = fix_address(data[:, 3])
    coords[:, 0] = fix_address(coords[:, 0])

    print(len(set(data[:, 3])), "unique placenames!")
    print("-"*50)
    print("\n".join(dheader))
    print("-"*50)
    print("\n".join(cheader))

    nf = 0
    plcvector = np.vectorize(str.lower)(coords[:, 0])
    for rendsz, szolghely, datum, hely, jelleg, megf in data:
        arg = np.argwhere((plcvector == hely.lower())).ravel()
        if len(arg) > 1:
            print("Arg > 1 for ", hely, ":", arg)
        elif len(arg) == 0:
            # print("Not found:", hely)
            x, y = ["none"] * 2
            nf += 1
        else:
            x, y = coords[arg[0], 1:3]

    print("Parsed: {}\nNot found: {}".format(len(data), nf))


if __name__ == '__main__':
    geocode_placenames()
