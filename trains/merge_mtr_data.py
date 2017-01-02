import os

from SciProjects.trains.utility import mtr_root as mtr


def sanity_check():
    numbers = "1234567890"
    assert "sum" in os.listdir(mtr)
    for fln in mtr + "sum/":
        assert fln[-4:] != ".csv", "Found csv file in 'sum/':\n{}".format(fln)
        assert fln[-8] == "_" and fln[-5:] == ".xlsx", "Found foreign file in 'sum/':\n{}".format(fln)
        assert fln[-7] in numbers and fln[-6] in numbers, "Found foreign file in 'sum/':\n{}".format(fln)
    print("Sanity check before MTR linenumber_objecttype_names merging passed!")


def parseone(categ):
    import openpyxl as xl

    chain = ""
    line_numbers = []
    number_of_columns = []
    fl_lst = [fl for fl in os.listdir(mtr + "sum/") if categ == fl[:-8]]
    for nfl, fl in enumerate(fl_lst):
        line_numbers.append(fl[-7:-5])
        ws = xl.load_workbook(fl).get_sheet_by_name("Munka1")
        for nrow, row in enumerate(ws.rows):
            if nrow == 0 and nfl > 0:
                continue
            ncell = 0
            for cell in row:
                ncell += 1
                if cell.value is not None:
                    chain += str(cell.value)
                chain += "\t"
            chain = chain[:-1] + "\n"
            number_of_columns.append(ncell)
    assert len(line_numbers) == len(set(line_numbers)), "Line number duplication!\n{}".format(line_numbers)
    if categ not in ("Kerítés", "Útátjáró"):
        assert len(set(number_of_columns)) == 1, "Difference in column numbers @ {}_{}.xlsx\n{}".format(
            categ, line_numbers[-1], number_of_columns)
    with open(categ + ".csv", "w") as fl:
        fl.write(chain)
        fl.close()
    print("Dumped", categ + "!")


def main():

    os.chdir(mtr + "sum")

    flz = os.listdir(".")
    flz = [fl for fl in flz if "nincs" not in fl and "~" not in fl]
    flz = [fl for fl in flz if fl[-5:] == ".xlsx"]

    categories = list(set([fl[:-8] for fl in flz]))

    for cat in categories:
        parseone(cat)

    print("Finished merging MTR tables!")


if __name__ == '__main__':
    from SciProjects.trains.utility import setup_environment
    setup_environment()
    # sanity_check()
    main()
