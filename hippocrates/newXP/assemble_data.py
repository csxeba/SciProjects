import os
import pickle

import numpy as np
from PIL import Image

dataroot = os.path.expanduser("~/Prog/data/raw/mr/")


def pull_sequence_to_array(root, ds=1):
    arz = []
    for fl in sorted(flnm for flnm in os.listdir(root) if flnm[-3:] == "bmp"):
        ar = np.asarray(Image.open(root+"/"+fl))[..., 0][..., None].astype("uint8")
        if ar.shape != (894, 661, 1):
            print("Invalid DIM:", ar.shape, end="")
            return None
        ar = ar[136:756, 72:572]
        if ds > 1:
            ar = ar[::ds, ::ds]
        arz.append(ar)

    if not arz:
        print("No pix!", end="")
        return None
    arz = np.stack(arz[:-4])
    switch = False
    while len(arz) > 40:
        arz = arz[:-1] if switch else arz[1:]
        switch = not switch
    if len(arz) < 40:
        print("Invalid ZDIM!", len(arz), end="")
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
    t2.append(pull_sequence_to_array(name+"/T2", ds=1))
    print()
t2 = np.stack(t2)
t2.dump("SM_T2pos.npa")
