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
                mapping[flnm] = (samplename, parallel)
    return mapping


if __name__ == '__main__':
    zviroot = "D:/tmp/PIC/"
    mapping = get_mapping(zviroot)
    for fl, (smp, prl) in sorted(mapping.items(), key=lambda it: it[0]):
        print("{}-{}/{}".format(fl, smp, prl))
