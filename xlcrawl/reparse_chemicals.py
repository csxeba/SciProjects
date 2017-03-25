from SciProjects.xlcrawl import project_root
from SciProjects.xlcrawl.util import pull_data, extract_inventory_numbers


def rstrip0s(string):
    if string[0] != "0":
        return string
    return rstrip0s(string[1:])


def strip0s(string):
    return rstrip0s(rstrip0s(string)[::-1])


def reparse_instruments():
    outchain = "FILE\tINSTRUMENT\tFORMATFIELD\tINVNUMBERS->\n"
    for line in pull_data("instrument.csv"):
        cnd, frm_field = extract_inventory_numbers(line[1])
        outchain += "\t".join(map(str, line[:2] + [frm_field] + cnd)) + "\n"

    with open(project_root + "invnumbers.csv", "w") as handle:
        handle.write(outchain)


def reparse_chemicals_by_inventory_id():
    cids = []
    for line in pull_data("vegyszerek.csv"):
        if line[1] == "-":
            continue
        cids.append(tuple(str(d).lower() for d in line[1:3] + [line[5]]))
    return sorted(list(set(cids)))


def filter_duplicates():
    outchain = "\n".join(
        "\t".join(line) for line in
        sorted(list(set(tuple(line) for line in pull_data("ChemTable.csv")))))
    with open(project_root + "ChemTable_uniq.csv", "w") as handle:
        handle.write(outchain)


if __name__ == '__main__':
    filter_duplicates()
