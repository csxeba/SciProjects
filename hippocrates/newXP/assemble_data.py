import os

import numpy as np
from PIL import Image


def pull_sequence_to_array(root):
    ar = np.array([np.asarray(Image.open(root+"/"+fl)) for fl in os.listdir(root) if fl[-3:] == "bmp"])
    switch = False
    while len(ar) > 45:
        ar = ar[:-1] if switch else ar[1:]
        switch = not switch
    if len(ar) < 45:
        print("Invalid number of frames!")
        return None
    return ar


dataroot = os.path.expanduser("~/Prog/data/raw/mr/")
os.chdir(dataroot)
names = os.listdir(".")
allnms = len(names)
t2 = []
for i, name in enumerate(sorted(names), start=1):
    print(f"{i}/{allnms} Reading {name}", end=" ")
    t2.append(np.array([pull_sequence_to_array(name+"/T2")]))
print()
t2 = np.array(t2)
t2.dump("SM_T2pos.npa")
