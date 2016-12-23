
def pull_data():
    from csxdata import roots
    from csxdata.utilities.parsers import parse_csv

    return parse_csv(roots["csvs"] + "mnb.csv", indeps=1, headers=1)

