import os

import numpy as np


def get_mapping(rootdir):
    mp = {}
    pjoin = os.path.join
    for samplename in sorted(os.listdir(rootdir)):
        for parallel in sorted(filter(
                lambda d: len(d) == 1,
                os.listdir(pjoin(rootdir, samplename)))):
            for flnm in sorted(filter(
                    lambda f: f[-4:] == ".zvi",
                    os.listdir(pjoin(rootdir, samplename, parallel)))):
                mp[flnm[:-4]] = (samplename, parallel)
    return mp


def get_xl_info(rootdir):
    import xlrd

    mp = get_mapping(rootdir)
    names = sorted(mp.keys())
    replicate = []
    xl_fls = {smplnm: [] for smplnm in names}
    flnmz = {smplnm: [] for smplnm in names}
    for smplnm in (s for s in os.listdir(rootdir) if len(s) == 4):
        xlname = [xl for xl in os.listdir(rootdir + smplnm) if xl[-4:] in ("xlsx", ".xls")][0]
        xlpath = rootdir + smplnm + "/" + xlname
        xl_fls[smplnm].append(xlpath)

        flz = []
        for root, dirs, fls in os.walk(rootdir + smplnm):
            got = [f[:-4] for f in fls if f[-4:] == ".zvi"]
            if len(got) > 0:
                replicate.append(int(root.split(os.sep)[-1]))
                flz += got
        flnmz[smplnm] += flz

    para1 = []
    para2 = []

    for smplnm in names:
        wbpath = xl_fls[smplnm]

        wb = xlrd.open_workbook(wbpath)
        ws = wb.sheet_by_index(0)
        print(ws.name)
        smplnm_fromxl = ws.cell(3, 0).value
        print(smplnm_fromxl)
        para1.append(np.array([ws.row(19)[i].value for i in range(1, 21)]))
        para2.append(np.array([ws.row(27)[i].value for i in range(1, 21)]))


if __name__ == '__main__':
    r = get_xl_info("D:/tmp/PIC/")
    print("FIN")
