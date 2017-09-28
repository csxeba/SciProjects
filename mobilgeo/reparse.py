import numpy as np

from csxdata.utilities.vectorop import argfilter
from SciProjects.mobilgeo.geocoding.placetypes import *


@np.vectorize
def fix_carno(carno: str):
    return carno.replace(" ", "").replace("-", "")


@np.vectorize
def fix_address(chain):
    return chain\
        .replace(",", " ")\
        .replace(".", " ")


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


def separate_classes(fileobj):

    def confirm(streamname, streamlen):
        print("Confirm objectification of the '{}' stream! ({} addresses)"
              .format(streamname, streamlen))
        return input("[y]/n > ").lower() != "n"

    def ktbtfilter(a):
        return ("külter" in a.lower() or
                "belter" in a.lower() or
                "kt" in a.lower() or
                "bt" in a.lower())

    def hrszfilter(a):
        return "hrsz" in a.lower() or "helyrajz" in a.lower()

    cache = AddressCache(projectroot + "cache/addresses.pkl")
    dothese = sorted(filter(lambda a: a not in cache, fileobj))
    ktbtstream = list(filter(ktbtfilter, dothese))
    hrszstream = list(filter(hrszfilter, dothese))
    nicestream = list(filter(lambda a: not (a in ktbtstream or
                                            a in hrszstream), dothese))

    objectify = []
    if confirm("Nice", len(nicestream)):
        objectify += [NiceAddress(addr, cache.set) for addr in nicestream]
    if confirm("HRSZ", len(hrszstream)):
        objectify += [HRSZ(addr, cache.set) for addr in hrszstream]
    if confirm("KTBT", len(hrszstream)):
        objectify += [KTBT(addr, cache.set) for addr in ktbtstream]
    if len(objectify) == 0:
        return
    list(map(cache.set, objectify))
    objectify += [cache.get(rawname) for rawname in
                  cache.dct if rawname not in dothese]
    cache.dump()
    return sorted(objectify, key=lambda a: a.rawname)


def geocode_placenames():
    inpath = projectroot + "Helyek.csv"
    with open(inpath) as handle:
        objects = separate_classes(handle)
        handle.close()

    try:
        handle = open(projectroot + "geocoded.csv", "r")
    except FileNotFoundError:
        addresses = []
        header = "RAW\tADDR\tX\tY\tFOUND\n"
    else:
        addresses = [line[-1] for line in handle]
        handle.close()
        header = ""

    with open(projectroot + "geocoded.csv", "a") as handle:
        handle.write(header)
        for i, obj in enumerate(objects, start=1):
            print(f"\rDoing {i:>4}/{len(objects)}", end="")
            if obj.address in addresses:
                print(" obj found in addresses!")
                continue
            obj.geocode()
            addresses.append(obj.address)
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
