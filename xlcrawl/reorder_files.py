from SciProjects.xlcrawl import project_root

import os
import shutil


def accumulate_files():
    xlflz = []
    for root, dirz, flz in os.walk(project_root):
        xlflz += [(root + "/", flnm) for flnm in flz if flnm[-4:] in ("xlsx", ".xls")]

    for drnm, flnm in xlflz:
        shutil.copy(drnm + flnm, project_root + "ALLXLFLZ/" + flnm)


def get_original_file_paths():
    path_database = {}
    for root, dirz, flz in os.walk(project_root):
        if any([project_root == root,
                "ALLXLFLZ" in root,
                "summations" in root,
                "Shiny" in root]):
            continue
        for fl in flz:
            if fl in path_database:
                raise RuntimeError("\n".join(
                    (fl + " already in dictionary!",
                     "IN: " + path_database[fl],
                     "CURRENT: " + root)))
            path_database[fl] = root
    return path_database


def create_target_directory_tree():
    pathdb = get_original_file_paths()
    destroot = "/data/Ideglenessen/onkoltseg_output/"
    for flnm in os.listdir(project_root + "ALLXLFLZ/"):
        for cat in ("vegyszer", "eszköz", "műszer", "fejléc"):
            try:
                os.makedirs(destroot + pathdb[flnm] + "/" + cat)
            except FileExistsError:
                continue
            except KeyError:
                print("OUTLIER:", flnm)
                continue


def redisperse_files(root, categ):
    pathdb = get_original_file_paths()
    jolly = []
    for flnm in os.listdir(root):
        if flnm not in pathdb:
            target = "/data/Ideglenessen/onkoltseg_output/KIMARADT/" + categ + "/" + flnm
        else:
            target = pathdb[flnm].replace(
                "Dokumentumok/onkoltseg", "Ideglenessen/onkoltseg_output"
            ) + "/" + categ + "/" + flnm

        source = root + flnm
        shutil.copy(source, target)
        jolly.append(flnm)
    print("\n".join([flnm for flnm in sorted(pathdb) if flnm not in jolly]))

if __name__ == '__main__':
    for dstcat, srccat in zip(("vegyszer", "eszköz", "műszer", "fejléc"),
                              ("chem", "item", "inst", "head")):
        redisperse_files(project_root + "Shiny/reparsed_" + srccat + "/", dstcat)
