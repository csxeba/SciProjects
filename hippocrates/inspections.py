import os

from csxdata import roots

hiporoot = roots["raw"] + "Project_Hippocrates/"
positives = os.listdir(hiporoot + "SM pozitív")
negatives = os.listdir(hiporoot + "SM negatív")


def print_names():
    print("POZITÍV: ")
    for pos in positives:
        print(pos, end=", ")
    print("\nNEGATÍV: ")
    for neg in negatives:
        print(neg, end=", ")
    print()


def print_number_of_pics():
    pics = dict()

    for name in positives:
        try:
            pcm = len(os.listdir(hiporoot + "SM pozitív/" + name + "/postCM"))
        except FileNotFoundError:
            print("NoDir+pCM: {}".format(name))
            pcm = "NoDir"
        try:
            t2 = len(os.listdir(hiporoot + "SM pozitív/" + name + "/t2.axi"))
        except FileNotFoundError:
            t2 = "NoDir"
            print("NoDir+t2 : {}".format(name))
        pics[name] = pcm, t2

    for name in negatives:
        try:
            pcm = len(os.listdir(hiporoot + "SM negatív/" + name + "/postCM"))
        except FileNotFoundError:
            pcm = "NoDir"
            print("NoDir-pCM: {}".format(name))
        try:
            t2 = len(os.listdir(hiporoot + "SM negatív/" + name + "/t2.axi"))
        except FileNotFoundError:
            t2 = "NoDir"
            print("NoDir-t2 : {}".format(name))
        pics[name] = pcm, t2

    print("NÉV\tpostCM\tt2.axi")
    for name in sorted(list(pics.keys())):
        pCM, t2 = pics[name]
        print(name, pCM, t2, sep="\t")

if __name__ == '__main__':
    print_number_of_pics()