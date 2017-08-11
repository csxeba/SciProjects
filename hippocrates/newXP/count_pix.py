import os

WORKDIR = "/home/csa/Letöltések/Térfoglalás/"
os.chdir(WORKDIR)
print("NAME", "T1", "T2", sep="\t")
for name in sorted(os.listdir(".")):
    print(name, end="\t")
    os.chdir(name)
    t1 = len(os.listdir("t1"))
    print(t1, end="\t")
    t2 = len(os.listdir("t2"))
    print(t2)
    os.chdir(WORKDIR)
