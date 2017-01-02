import os

from SciProjects.trains.utility import inka_root as inka
from SciProjects.trains.utility import mtr_root as mtr
from SciProjects.trains.utility import headers_root as headers
from SciProjects.trains.utility import dataroot
from SciProjects.trains.utility import setup_environment
from SciProjects.trains.merge_mtr_data import main as mtrmain


def sanity_check(act=False):
    error = {1: "Directory: sum missing!",
             2: "Merged-linenumber_objecttype_names csv files are not present!",
             3: "Headers already extracted!"}

    errorcode = 0
    sumflz = os.listdir(mtr + "sum/")
    if "sum" not in os.listdir(mtr):
        errorcode = 1
    elif ".csv" not in " ".join(sumflz):
        errorcode = 2

    if "mtr_headers.csv" in sumflz and "inka_headers.csv" in os.listdir(inka + "Pálya/"):
        errorcode = 3

    if not act:
        assert not errorcode, error[errorcode]
        print("Sanity check before pulling headers passed!")
    else:
        if errorcode:
            print(error[errorcode])
            setup_environment()
            mtrmain()
        else:
            print("Sanity check before pulling headers passed!")


def from_mtr():
    os.chdir(mtr + "sum/")
    flz = [flname for flname in os.listdir(".") if ".csv" == flname[-4:]]

    for fl in flz:
        objecttype = fl[:-4]
        with open(fl) as f:
            header = f.readlines()[0]
            f.close()
        with open("mtr_headers.csv", mode='a') as f:
            f.write(objecttype + "\t" + header)
            f.close()

    print("Generated mtr_headers.csv @ {}".format(os.getcwd()))


def from_inka():
    import openpyxl as xl

    os.chdir(inka + "/Pálya")
    for fl in [flnm for flnm in os.listdir(".") if flnm[0] != "~"]:
        objecttype = fl[:-16]
        wb = xl.load_workbook(fl)
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        header = "\t".join([str(cell.value) for cell in ws.rows[0]])
        header.replace("None", "")
        with open("inka_headers.csv", "a") as f:
            f.write(objecttype + "\t" + header + "\n")
            f.close()

    print("Generated inka_headers.csv @ {}".format(os.getcwd()))


def relocate_header_files():
    from shutil import copy2

    assert "inka_headers.csv" in os.listdir(inka + "Pálya/") and \
        "mtr_headers.csv" in os.listdir(mtr + "sum/"), \
        "Headers not yet extracted!"
    assert "headers" in os.listdir(dataroot), "<headers> directory not present in " + dataroot
    assert "inka_headers" not in os.listdir(headers) or "mtr_headers" not in os.listdir(headers), \
        "One or more header files is already present in " + headers

    copy2(inka + "Pálya/inka_headers.csv", headers)
    copy2(mtr + "sum/mtr_headers.csv", headers)
    print("Relocated INKA and MTR headers to", headers)


def main(force_update=False):
    if force_update:
        setup_environment()
        mtrmain()
    sanity_check()
    from_mtr()
    from_inka()
    relocate_header_files()

    print("Finished pulling headers from MTR and INKA!")


if __name__ == '__main__':
    main(force_update=True)
