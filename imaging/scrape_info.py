import os


def get_mapping(rootdir):
    mapping = {}
    pjoin = os.path.join
    for samplename in sorted(filter(
            lambda d: len(d) == 4,
            os.listdir(rootdir))):
        for parallel in sorted(filter(
                lambda d: len(d) == 1,
                os.listdir(pjoin(rootdir, samplename)))):
            for flnm in sorted(filter(
                    lambda f: f[-4:] == ".zvi",
                    os.listdir(pjoin(rootdir, samplename, parallel)))):
                mapping[flnm[:-4]] = (samplename, parallel)
    return mapping


def get_xl_info(rootdir):
    import openpyxl

    mapping = get_mapping(rootdir)
    xl_fls = {smplnm: rootdir + smplnm + "/" + [xl for xl in os.listdir(rootdir) if xl[-4:] in ("xlsx", ".xls")][0]
              for smplnm in sorted(mapping.keys())}

    for wbpath in (path for smplnm, path in sorted(xl_fls.items(), key=lambda x: x[0])):
        wb = openpyxl.load_workbook()
        ws = wb[0]


if __name__ == '__main__':
    zviroot = "D:/tmp/PIC/"
    mapping = get_mapping(zviroot)
    for fl, (smp, prl) in sorted(mapping.items(), key=lambda it1: it1[0]):
        print("{}-{}/{}".format(fl, smp, prl))
