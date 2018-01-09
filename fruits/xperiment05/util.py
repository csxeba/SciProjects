import pandas as pd

from SciProjects.fruits import projectroot


def pull_data(label):
    features = ["DH1", "DH2", "D13C"]
    df = pd.read_excel(projectroot + "Gyümölcs_adatbázis_összesített.xlsx")  # type: pd.DataFrame
    df.dropna(subset=[label] + features, inplace=True)
    return df[[label] + features]
