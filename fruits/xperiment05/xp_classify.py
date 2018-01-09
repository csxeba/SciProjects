import pandas as pd

from csxdata.learning.supervised import SupervisedSuite

from SciProjects.fruits import projectroot


df = pd.read_excel(projectroot + "Gyümölcs_adatbázis_összesített.xlsx")  # type: pd.DataFrame

suite = SupervisedSuite()
suite.run_experiments(df, labels=["MEGYE", "EV", "FAMILIA"], features=["DH1", "DH2", "D13C"],
                      outxlsx=projectroot + "SUPERVISED_XP_RESULTS.xlsx")
