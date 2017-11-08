from collections import defaultdict

import numpy as np
import pandas as pd

from SciProjects.methodmatrix import projectroot


def extract_hstring(string):
    string = str(string)
    string = string.replace("(", "").replace(")", "").replace("  ", " ")
    names = string.split(", ")
    return set(" ".join(w.strip() for w in name.split(" ") if not w.isdigit() and w) for name in names)


def extract_names(row):
    output = set()
    output.add(str(row["OWNER"]))
    output.add(str(row["MNAME"]))
    output.add(str(row["TNAME"]))
    output.update(extract_hstring(row["MHSTR"]))
    output.update(extract_hstring(row["THSTR"]))
    if "nan" in output:
        output.remove("nan")
    return output


def main():
    df = pd.read_excel(projectroot + "headerdata.xlsx")  # type: pd.DataFrame
    staff = pd.read_excel(projectroot + "allomany.xlsx")["Név"].tolist()
    col = ["MID", "DJNM"] + staff
    data = []
    for i, row in df.iterrows():
        mID = str(row["MID"])
        print("Doing", mID)
        names = list(extract_names(row))
        akkr = not pd.isnull(row["AKN"])
        values = [mID, row["DJNM"]] + [((2 if akkr else 1) if name in names else 0) for name in staff]
        data.append(values)
    pd.DataFrame(data=data, columns=col).to_excel(projectroot + "StaffMatrix.xlsx")


if __name__ == "__main__":
    main()
