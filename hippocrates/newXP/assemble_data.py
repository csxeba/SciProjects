import os

import numpy as np
from PIL import Image


def pull_sequence_to_array(root):
    arz = []
    for fl in (flnm for flnm in os.listdir(root) if flnm[-3:] == "bmp"):
        ar = np.asarray(Image.open(root+"/"+fl)).sum(axis=2, keepdims=True)
        if ar.shape != [894, 661, 1]:
            print("Invalid DIM:", ar.shape)
            return None
        arz.append(ar)
    arz = np.stack(arz)
    switch = False
    while len(arz) > 45:
        arz = arz[:-1] if switch else arz[1:]
        switch = not switch
    if len(arz) < 45:
        print("Invalid ZDIM!")
        return None
    return arz


dataroot = os.path.expanduser("~/Prog/data/raw/mr/")
os.chdir(dataroot)
names = os.listdir(".")
allnms = len(names)
t2 = []
for i, name in enumerate(sorted(names), start=1):
    print(f"{i}/{allnms} Reading {name}", end=" ")
    t2.append(np.array([pull_sequence_to_array(name+"/T2")]))
    print()
t2 = np.array([tensor for tensor in t2 if tensor is not None])
t2.dump("SM_T2pos.npa")
