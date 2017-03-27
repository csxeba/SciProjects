from csxdata import roots, CData

wineframe = CData(roots["csv"] + "sophiewine.csv", cross_val=0,
                  indeps=4, headers=1, feature="COUNTRY",
                  decimal=True)
