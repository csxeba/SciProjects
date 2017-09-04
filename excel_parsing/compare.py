from datetime import datetime
from difflib import SequenceMatcher

import numpy as np
import pandas as pd

from SciProjects.excel_parsing import projectroot


def daterange_firstday(weirdstring):
    weirdstring = str(weirdstring)
    y, m = int(weirdstring[:4]), int(weirdstring[4:])
    return datetime(y, m, 1)


@np.vectorize
def strsim(str1, str2):
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


def strsim_vec(str1, strvec):
    return strsim(str1, strvec)


beerk = pd.read_excel(projectroot + "Compare_src/BEERK_2017.xlsx")  # type: pd.DataFrame
igeny = pd.read_excel(projectroot + "Compare_src/IGENY_2017.xlsx")  # type: pd.DataFrame

head = ["MSACC", "MEGNEV", "JELLEG", "MENNY", "DIM", "TELJESÜLT", "DÁTUM",
        "SIM", "BROWID", "BCIKKSZ", "BMEGNEV", "BJELLEG", "NÖV", "NDIM", "IDŐ"]
data = [head]
ln = len(igeny["MEGNEV"])
strln = len(str(ln))
browID_arg = set()
for i, igenyrow in igeny.iterrows():
    igenynev = igenyrow["MEGNEV"]
    print(f"\r{i:>{strln}}/{ln} - {igenynev}", end="")
    sims = strsim_vec(igenynev, beerk["MEGNEV"])
    args = sims.argsort().tolist()
    mxarg = args.pop()
    while mxarg in browID_arg:
        mxarg = args.pop()
    browID_arg.add(mxarg)
    outsim = sims[mxarg].round(4)
    megf = beerk.iloc[mxarg]
    if outsim < 0.55 or daterange_firstday(megf["IDŐ"]) < igenyrow["DÁTUM"]:
        data.append(list(igenyrow) + ["NINCS MEGFELELÉS!"] + ["" for _ in range(7)])
    else:
        data.append(list(igenyrow) + [outsim] + list(megf))
print()

chain = "\n".join("\t".join(map(str, line)) for line in data)
print(chain)
print(chain, file=open(projectroot + "matched.csv", "w"))
