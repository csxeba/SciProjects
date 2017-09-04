import os

import numpy as np
from PIL import Image

dataroot = os.path.expanduser("~/SciProjects/Project_Hippocrates/data/sinem/")


def pull_sequence_to_array(root):
    arz = []
    for fl in sorted(flnm for flnm in os.listdir(root) if flnm[-3:] == "bmp"):
        arz.append(np.asarray(Image.open(root + "/" + fl))[..., 0][..., None].astype("uint8"))

    if not arz:
        print("No pix!", end="")
        return None
    arz = np.stack(arz[:-4])
    switch = False
    while len(arz) > 39:
        arz = arz[:-1] if switch else arz[1:]
        switch = not switch
    if len(arz) < 39:
        print("Invalid ZDIM!", len(arz))
        return None
    arz = arz.T
    print("Final dim (x, y, z):", arz.shape, end=" ")
    return arz


os.chdir(dataroot)
names = os.listdir(".")
allnms = len(names)
t2 = []
for i, name in enumerate(sorted(names), start=1):
    print(f"{i:>2}/{allnms} Reading {name}", end=" ")
    retval = pull_sequence_to_array(name+"/T2")
    if retval is None:
        continue
    t2.append(retval)
    print()
t2 = np.stack(t2)
t2.dump("Sinem2_T2.npa")
