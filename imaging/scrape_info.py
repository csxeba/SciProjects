import os


class Sample:

    """
    Abstraction of a sample parallel.

    This corresponds to a zvi project file,
    and a jpeg image, generated from the zvi.
    It may have already been examined manually,
    in which case an excel file can be supplied,
    containing the results of the manual method.
    """

    def __init__(self, zviroot, name=None, jpegroot=None, parallel=None, xlpath=None):
        self.zviroot = zviroot
        self.name = name
        self.jpegroot = jpegroot
        self.xlpath = xlpath
        self.parallel = parallel
        self.jpegs = []

    def connect_the_dots(self):
        splitroot = os.path.split(self.zviroot)
        if self.name is None:
            name = splitroot[-2]
            assert len(name) == 4
            self.name = splitroot[-2]
        if self.parallel is None:
            prl = splitroot[-1]
            assert all(("0" <= c <= "9" for c in prl))
            self.parallel = prl


root = "D:/tmp/jpegs"
sep = os.path.sep

flz = []
for path, dirs, fls in os.walk(root):
    flz += [(path, fl[:-4]) for fl in fls if fl[-4:] == ".zvi"]

info = {}
for path, flnm in flz:
    members = path.split(sep)
    smpl, prll = members[-2:]
    info[flnm] = (path, smpl, prll)