from csxdata import roots

labels = (
    "grapes", "gyumolcs", "kozma", "gyumzsind",
    "fcvnyers", "burleynyers", "mnb"
)
indepsn = (6, 6, 0, 0, 1, 1, 2)

paths = {lab: tuple(zip(roots["csvs"] + lab + ".csv", ind))
         for lab, ind in zip(labels, indepsn)}
