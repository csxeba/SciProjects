from .misc import *


def sanity_check():
    from csxdata import roots
    from os import listdir, path

    projectroot = roots["ntabpics"]
    assert path.exists(projectroot)
    assert ".jpg" in "".join(listdir(projectroot))
    print("Sanity check passed!")

sanity_check()
