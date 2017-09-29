
def pull_data():
    from csxdata import roots
    from csxdata.utilities import parser

    return parser.csv(roots["csvs"] + "mnb.csv", indeps=2, headers=1, feature="Name",
                      lower=True, sep="\t")
