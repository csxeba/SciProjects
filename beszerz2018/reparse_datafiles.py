import numpy as np
import pandas as pd

from SciProjects.beszerz2018 import projectroot, os


def parse(path):
    data = pd.read_excel(path)  # type: pd.DataFrame
    cikksz = None
    dx, dy = data.shape
    strln = len(str(dx))
    for i, cikk in enumerate(data["CIKKSZÁM"]):
        print(f"\rRow: {i+1:>{strln}}/{dx}", end="")
        if pd.isnull(cikk):
            data["CIKKSZÁM"][i] = cikksz
        else:
            cikksz = cikk
            data["CIKKSZÁM"][i] = np.nan
    print("\nDumping XL...")
    data = data[~pd.isnull(data["MOZGÁSNEM"])]
    flnm = f"parsed_{'vegy' if 'VEGY' in path else 'eszk'}_{'2016' if '2016' in path else '2017'}.xlsx"
    data.to_excel(projectroot + "reparsed/" + flnm)


if __name__ == '__main__':
    for file in os.listdir(projectroot + "raw/"):
        parse(projectroot + "raw/" + file)
