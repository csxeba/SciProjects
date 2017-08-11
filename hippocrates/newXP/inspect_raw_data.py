import os

dataroot = os.path.expanduser("~/SciProjects/Project_Hippocrates/data/")
print("NÉV;T1;T2;DIAG")
for diag in os.listdir(dataroot):
    for sample in os.listdir(dataroot + diag):
        if sample == "meta.txt":
            continue
        T1 = len(os.listdir(dataroot + diag + "/" + sample + "/T1"))
        T2 = len(os.listdir(dataroot + diag + "/" + sample + "/T2"))
        print(sample, T1, T2, diag, sep=";")
