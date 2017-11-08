import numpy as np
import pandas as pd

from SciProjects.suppliers import projectroot


def namestring(row):
    return "\n".join([row["name"], row["address"], "Tel.:" + row["phone"],
                      "Fax:" + row["fax"], "E-mal:" + row["email"]])


def servstring(row):
    nice = []
    if row["MBESZ"] == "X": nice.append("műszer beszerzés")
    if row["MKARB"] == "X": nice.append("karbantartás")
    if row["MKAL"] == "X": nice.append("kalibrálás")
    if row["EBESZ"] == "X": nice.append("készlet beszerzés")
    if row["VBESZ"] == "X": nice.append("vegyszer beszerzés")
    if row["CRM"] == "X": nice.append("anyagminta, CRM beszerzés")
    if row["JÁRTAS"] == "X": nice.append("jártassági vizsgálat")
    if not nice:
        return ""
    nice[0] = nice[0].capitalize()
    return "\n".join(nice)


def m_id_string(row):
    na = row["NAKKR"]
    a = row["AKKR"]
    na = [] if pd.isnull(na) else str(na).split(", ")
    a = [] if pd.isnull(a) else str(a).split(", ")
    return ", ".join(sorted(na + a))


def get_rating(row):
    rate = row["ÁTLAG"]
    if pd.isnull(rate):
        return ""
    rate = int(rate)
    return ["NULL", "ELÉGTELEN", "ELÉGSÉGES", "KÖZEPES", "JÓ", "KIVÁLÓ"][rate]


report_header = ("Beszállító neve", "Tárgy, szolgáltatás megnevezése", "Vizsgálat sorszáma",
                 "Értékelők aláírása", "Értékelés időpontja", "Minősítés", "Megjegyzés")

suppliers = pd.read_excel(projectroot + "suppliers_reparsed.xlsx")
summary = pd.read_excel(projectroot + "Summary.xlsx")
outdata = []
for i, sumrow in summary.iterrows():
    outdata.append([sumrow["CÉG"], servstring(sumrow), m_id_string(sumrow), None, None, get_rating(sumrow), None])
outdata = np.array(outdata)
pd.DataFrame(data=outdata, columns=report_header).to_excel(projectroot + "FINAL.xlsx")
