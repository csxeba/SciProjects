import os

import numpy as np
import nmrglue as ng
from matplotlib import pyplot as plt


projectroot = "/home/csa/SciProjects/NMRCONVERT/"
C = ng.convert.converter()


def convertdir(inroot, outroot):
    for dirnm in os.listdir(inroot):
        print("Doing", dirnm)
        vvals = ng.varian.read(inroot + dirnm)
        C.from_varian(*vvals)
        ng.bruker.write(outroot + dirnm, *C.to_bruker())
    print("\n -- end program --")


def plotfl(path):
    meta, data = ng.varian.read(path)
    if data.ndim == 1:
        ft = np.fft.fft(data)
        plt.plot(ft.imag, "r-")
        plt.plot(ft.real, "b-")
    elif data.ndim == 2:
        plt.imshow(data.real)
    else:
        raise RuntimeError("NDIM: " + str(data.ndim))
    plt.show()


if __name__ == '__main__':
    plotfl(projectroot + "nszkk/proton_integral.fid")
