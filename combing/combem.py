import os

import numpy as np
import pandas as pd

from SciProjects.combing import projectroot


vegyhead = ["SSZ", "CIKKSZ", "MEGNEV", "CAS", "NOPE1", "NOPE2", "MENNY", "MINŐS",
            "KISZER", "MENNYEGY", "SZERSZER", "HALMAZ", "FORG1", "FORG2", "FORG3",
            "KIZÁR", "KAPCSOL", "INDOK", "MEGJ"]
eszkhead = ["SSZ", "CIKKSZ", "MEGNEV", "NOPE1", "NOPE2", "MENNY", "MINŐS", "MENNYEGY",
            "FORG1", "FORG2", "FORG3", "KIZÁR", "KAPCSOL", "INDOK", "MEGJ"]


def guessmode(path):
    if "Eszköz" in path:
        return "eszk"
    elif "Vegyszer" in path:
        return "vegy"
    raise RuntimeError("Invalid filename!\n" + path)


def setID(df, mode):
    if mode == "eszk":
        df["ID"] = np.vectorize(lambda s1, s2: s1 + s2)(
            df["MEGNEV"].astype(str), df["MINŐS"].astype(str)
        )
    else:
        df["ID"] = np.vectorize(lambda s1, s2, s3: s1 + s2 + s3)(
            df["MEGNEV"].astype(str), df["MINŐS"].astype(str), df["KISZER"].astype(str)
        )


def read_table(path):
    mode = guessmode(path)
    header = eszkhead if mode == "eszk" else vegyhead
    df = pd.read_excel(path, skiprows=2, header=1)  # type: pd.DataFrame
    df = df.iloc[:, :len(header)]
    df.columns = header
    df = df[df["MENNY"] > 0 & ~np.isnan(df["MENNY"])]
    setID(df, mode)
    return df


def pull_bases():
    eszk = read_table(projectroot + "Base/Eszköz_beszerzés_2018.xlsx")
    vegy = read_table(projectroot + "Base/Vegyszer_beszerzés_2018.xlsx")
    return eszk, vegy


def append_extra(path, vegybase, eszkbase):
    mode = guessmode(path)
    base = eszkbase if mode == "eszk" else vegybase  # type: pd.DataFrame
    df = read_table(path)
    for i, ID in enumerate(df["ID"]):
        count = (ID == base["ID"]).sum()
        if count > 1:
            raise RuntimeError(f"Duplicates: {ID}")
        if count == 0:
            base.append(df.iloc[i])


if __name__ == '__main__':
    eb, vb = pull_bases()
    os.chdir(projectroot + "Extra")
    for extra in os.listdir("."):
        print("Doing", extra)
        append_extra(extra, vb, eb)
    vb.to_excel(projectroot + "VegyFIN.xlsx", columns=[h for h in vegyhead if h[:4] != "NOPE"])
    eb.to_excel(projectroot + "EszFIN.xlsx", columns=[h for h in eszkhead if h[:4] != "NOPE"])
