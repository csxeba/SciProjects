import os

import xlrd as xl
from xlrd.sheet import Sheet
import pandas as pd

from SciProjects.suppliers import resourceroot, rawroot, projectroot


def extract_header(ws: Sheet):
    return (ws.cell_value(1, 1)), (ws.cell_value(1, 6))


def extract_ratings(wb, sheet):
    df = pd.read_excel(wb, engine="xlrd", sheetname=sheet, header=2, skiprows=[0, 1])  # type: pd.DataFrame
    return df.iloc[:, :6].dropna().as_matrix()


def build_df(name, date, table):
    rating = pd.DataFrame(columns=["Név", "Dátum"] + aspects)
    for colnm, col in zip(aspects, table.T):
        rating[colnm] = col
    rating["Név"] = name
    rating["Dátum"] = date
    return rating


def build_frames(wb):
    vegytable = extract_ratings(wb, "Vegyszer")
    eszktable = extract_ratings(wb, "Műszer")
    vname, vdate = extract_header(wb.sheet_by_name("Vegyszer"))
    ename, edate = extract_header(wb.sheet_by_name("Műszer"))
    assert vname == ename
    assert vname
    return build_df(vname, vdate, vegytable), build_df(ename, edate, eszktable)


aspects = ["Beszállító", "Minőségi színvonal", "Beszállítási/elintézési idő",
           "Ár", "Kapcsolattartás", "Szakmai felkészültség"]
vegydf = pd.DataFrame(columns=["Név", "Dátum"] + aspects)
eszkdf = pd.DataFrame(columns=["Név", "Dátum"] + aspects)

for xlfl in (flnm for flnm in os.listdir(rawroot) if flnm[-5:] == ".xlsx"):
    print("Reading", xlfl)
    try:
        wb = xl.open_workbook(rawroot + xlfl)
    except Exception as E:
        print("CAUGHT:", str(E))
        continue
    vdf, edf = build_frames(wb)
    vegydf = vegydf.append(vdf, ignore_index=True, verify_integrity=True)
    eszkdf = eszkdf.append(edf, ignore_index=True, verify_integrity=True)

vegydf.to_excel(projectroot + "Merged_vegy.xlsx")
eszkdf.to_excel(projectroot + "Merged_eszk.xlsx")
