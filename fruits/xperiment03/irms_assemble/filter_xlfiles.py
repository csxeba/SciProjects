import os
import shutil
from collections import defaultdict

from fruits.xperiment03.irms_assemble import projectroot


class Sorter:

    targetflz = set()
    targetpath = projectroot + "Current/"
    duplicates = defaultdict(int)

    @staticmethod
    def filter_files_from_directory(source_dirpath):
        xlflz = [flnm for flnm in os.listdir(source_dirpath) if flnm[-4:] in (".xls", "xlsx")]
        N = len(xlflz)
        strln = len(str(N))
        for i, xlfl in enumerate(xlflz, start=1):
            print(f"{i:>{strln}}/{N} - {source_dirpath}{xlfl}")
            if xlfl[:2] not in ("14", "15", "16", "17"):
                continue
            trgfl = xlfl[:]
            if xlfl in Sorter.targetflz:
                print("Name collision!:", source_dirpath + xlfl)
                Sorter.duplicates[xlfl] += 1
                trgfl = trgfl + "_" + str(Sorter.duplicates[xlfl]).rjust(3, "0")
            shutil.move(source_dirpath + xlfl, Sorter.targetpath + trgfl)
            Sorter.targetflz.add(xlfl)


if __name__ == '__main__':
    for dirnm in ("IRMS_Eredmények", "LABORKOZOS_IRMS_eredmények", "RFT_IRMS_eredmenyek"):
        print(f" !! DOING {projectroot}{dirnm}/...")
        Sorter.filter_files_from_directory(projectroot + dirnm + "/")
        print()
