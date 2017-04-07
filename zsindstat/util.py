from csxdata import CData


DEFAULTPATH = "/home/csa/SciProjects/Project_zsindely/zsindsum.csv"

axlab = ("DH1", "D13C")
axlab_latex = (r"$(D/H)_I$", r"$\delta^{13}C$")


def pull_data(feature, path=DEFAULTPATH, **kw):
    return CData(path, indeps=6, headers=1, cross_val=0,
                 dehungarize=True, decimal=True,
                 feature=feature, **kw)

