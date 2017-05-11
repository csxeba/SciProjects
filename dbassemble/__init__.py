from os.path import expanduser

projectroot = expanduser("~/SciProjects/Project_DBbuild/")
sourceroot = expanduser("~/Lezárt/onkoltseg/")

ranges = {
    "djnum": "4", "djname": "5", "owner": "6",
    "mname": "9", "akknums": "10", "mnum": "11",
    "mernok": "14", "mtasz": "15", "mhour": "16",
    "hmernok": "17",
    "techn": "19", "ttasz": "20", "thour": "21",
    "htechn": "22",
    "vnumstr": "25"
}
ranges = {k: "B" + v for k, v in ranges.items()}
