from csxdata import roots

labels = (
    "grapes", "kozma", "gyumzsind",
    "fcvnyers", "burleynyers", "mnb")

indepsn = (6, 4, 3, 1, 1, 2)

paths = {lab: (roots["csvs"] + lab + ".csv", ind)
         for lab, ind in zip(labels, indepsn)}
