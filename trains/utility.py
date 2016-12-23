import os
import sys

dataroot = "/data/Ideglenessen/INKA_Adatrendezés/" if sys.platform != "win32" else "D:/Data/raw/Project_MAV/"
mtr_root = dataroot + "MTR_ből_leszedett_adatok/"
nkh_root = dataroot + "NKH_Adatrendezés/"
inka_root = dataroot + "INKA/"
headers_root = dataroot + "headers/"
tmp_root = dataroot + ".csxcache/"


class _Roots:
    def __init__(self):
        self.roots = {"data": dataroot,
                      "mtr": mtr_root,
                      "nkh": nkh_root,
                      "inka": inka_root,
                      "headers": headers_root,
                      "header": headers_root,
                      "tmp": tmp_root,
                      "temp": tmp_root}

    def __getitem__(self, x):
        if not isinstance(x, str):
            raise TypeError("Expected string, got {}".format(type(x)))
        x = x.lower()
        if x in self.roots:
            return self.roots[x]
        else:
            raise IndexError("No path specified for {}".format(x))

    def __call__(self, x):
        return self[x]


roots = _Roots()


def setup_environment():

    def mtr_dirchecker():
        print("Purging MTR/sum directory from deviations!")
        numbers = "1234567890"
        filelist = os.listdir(mtr_root + "sum/")

        for fln in filelist:
            if ".csv" == fln[-4:]:
                print("Warning! Found csv file(s) in 'sum/'! Removing...")
                [os.remove(mtr_root + "sum/" + f) for f in filelist if ".csv" == f[-4:]]
                mtr_dirchecker()
                break
            elif (fln[-8] != "_" or fln[-5:] != ".xlsx") or \
                    (fln[-7] not in numbers and fln[-6] not in numbers):
                print("Warning! Found foreign file in 'sum/' Removing...")
                os.remove(mtr_root + "sum/" + fln)
            elif "nincs" in fln:
                print("Warning! Found empty file! Removing...")
                [os.remove(mtr_root + "sum/" + f) for f in filelist if "nincs" in f]
                mtr_dirchecker()
                break
            elif "~" == fln[0]:
                print("Warning! Found MSOffice lock file! Removing...")
                [os.remove(mtr_root + "sum/" + f) for f in filelist if "~" == f[0]]
                mtr_dirchecker()
                break

    def inka_dirchecker():
        print("Purging INKA/Pálya directory from deviations!")

        filelist = os.listdir(inka_root + "Pálya/")

        for fln in filelist:
            if ".csv" == fln[-4:]:
                print("Warning! Found csv file(s) in INKA/Pálya! Removing...")
                [os.remove(inka_root + "Pálya/" + f) for f in filelist if ".csv" == f[-4:]]
                inka_dirchecker()
                break
            elif fln[-16:] != "_2016.06.30.xlsx":
                print("Warning! Found foreign file in INKA/Pálya! Removing...")
                os.remove(inka_root + "Pálya/" + fln)
            elif "~" == fln[0]:
                print("Warning! Found MSOffice lock file in INKA/Pálya! Removing...")
                [os.remove(inka_root + "Pálya/" + f) for f in filelist if "~" == f[0]]
                inka_dirchecker()
                break

    def create_sumdir():
        print("Creating and filling <sum> directory...")
        os.mkdir(mtr_root + "sum")
        assemble_files_recursively(source=mtr_root, destination=mtr_root+"sum/", extension=".xlsx")

    if "sum" in os.listdir(mtr_root):
        from shutil import rmtree
        print("Removing existing <sum> directory...")
        rmtree(mtr_root + "sum")
    create_sumdir()
    mtr_dirchecker()
    inka_dirchecker()
    print("Environment is set up for MTR data merge and header data extraction!")


def assemble_files_recursively(source, destination, extension=".xlsx"):
    from shutil import copy2

    print("Files from subfolders to", destination)

    assert extension[0] == ".", "Please supply a valid extension format: '.something'"
    walk = os.walk(top=source)  # lists directory contents recursively from top to bottom
    for dirpath, dirnames, flnames in walk:
        if not flnames:
            continue
        if "sum" in dirpath:
            continue
        for fl in flnames:
            if extension == fl[-len(extension):] and "útátjáró" not in fl:
                copy2(dirpath + "/" + fl, destination)


if __name__ == '__main__':
    assemble_files_recursively(source=mtr_root, destination=mtr_root + "sum/", extension=".xlsx")


"""TODO:

Handle the xlsx/xls problem!
Handle the missing .csxcache folder problem!
Investigate what's wrong with <Útátjáró> and <Kerítés>!
Check whether the extracted NKH data is valid!
It is certain that the headers are weird... Maybe hardcode the layouts?
"""