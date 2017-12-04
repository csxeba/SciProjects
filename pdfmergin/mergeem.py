import os

from SciProjects.pdfmergin import projectroot
import subprocess


def extract_version(file):
    spl = file.split(" ")
    version = spl[0].replace("-", "_")
    for i, lt in enumerate("abcdefgh", start=1):
        version = version.replace(lt, str(i))
    # noinspection PyRedeclaration
    vspl = version.split("_")
    vspl = vspl + ["0" for _ in range(4 - len(vspl))]
    vspl = [f"{vn:0>2}" for vn in vspl]
    return "_".join(vspl)


def rename():
    os.chdir("raw")
    oldnames = os.listdir(".")
    for oldname, newname in sorted(zip(oldnames, map(extract_version, oldnames)), key=lambda result: result[1]):
        print(oldname, newname, sep=" -> ")
        os.rename(f"{oldname}", f"{newname}.pdf")
    os.chdir(projectroot)


def unite():
    pass


if __name__ == '__main__':
    os.chdir(projectroot)
    rename()
