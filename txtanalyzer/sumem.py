import os

os.chdir("D:\\tmp\\diff\\")

prps = (fl for fl in sorted(os.listdir(".")) if fl[:3] == "prp" and fl[-4:] == ".txt")
oris = (fl for fl in sorted(os.listdir(".")) if fl[:3] == "ori" and fl[-4:] == ".txt")

prpchain = ""
for prpfl in prps:
    with open(prpfl, encoding="utf-8-sig") as fl:
        prpchain += fl.read()

orichain = ""
for orifl in oris:
    with open(orifl, encoding="utf-8-sig") as fl:
        orichain += fl.read()


with open("ori.txt", "w") as oriout:
    oriout.write(orichain)

with open("prp.txt", "w") as prpout:
    prpout.write(prpchain)

