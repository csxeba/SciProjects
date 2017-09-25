import openpyxl as xl

from SciProjects.fruits import projectroot


def parse_xlfl(path):
    wb = xl.load_workbook(path, data_only=True)
    for sheetname in wb.sheetnames:
        ws = wb.get_sheet_by_name(sheetname)
        ID = sheetname.split(" ")[0]
        if not ID.isdigit() or len(ID) != 8:
            continue
        print(ID, end="\t")
        for rown in range(23, 33):
            print(ws.cell("R" + str(rown)).value, end="\t")
        print()


if __name__ == '__main__':
    parse_xlfl(projectroot + "Kozma_nyers/Pálinka.adatbázis.2016.xlsx")
