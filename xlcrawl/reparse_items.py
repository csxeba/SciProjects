from SciProjects.xlcrawl import project_root
from SciProjects.xlcrawl.util import pull_data, extract_inventory_numbers

# FILE	NAME	QUANT


def get_inventory_numbers(raw_line):
    if "vizsgálat esetében minden" in "".join(raw_line):
        return ["-"], "-", "-"
    candidates = []
    oldfield = raw_line[1]
    if len(raw_line) >= 3:
        for field in raw_line[2:]:
            candidates, newfield = extract_inventory_numbers(field)
            if candidates:
                break

    if not candidates:
        candidates, newfield = extract_inventory_numbers(oldfield)
    else:
        _, newfield = extract_inventory_numbers(oldfield)

    return list(map(str, candidates)), oldfield, newfield


def reparse_items():
    outchain = "FILE\tOLDFIELD\tNEWFIELD\tINVNUMBERS->\n"
    for line in pull_data("items.csv"):
        cnd, moldy, shiny = get_inventory_numbers(line)
        outchain += "\t".join([line[0]] + [moldy, shiny] + cnd) + "\n"
    with open(project_root + "itemparsed.csv", "w") as handle:
        handle.write(outchain)


def reparse_instruments():
    outchain = "FILE\tOLDFIELD\tNEWFIELD\tINVNUMBERS->\n"
    for line in pull_data("instrument.csv"):
        cnd, moldy, shiny = get_inventory_numbers(line)
        outchain += "\t".join([line[0]] + [moldy, shiny] + cnd) + "\n"
    with open(project_root + "instruments_parsed.csv", "w") as handle:
        handle.write(outchain)


def reparse_chemicals():
    outchain = "FILE\tOLDFIELD\tNEWFIELD\tINVNUMBERS->\n"
    for line in pull_data("chemicals.csv"):
        cnd, moldy, shiny = get_inventory_numbers(line)
        outchain += "\t".join([line[0]] + [moldy, shiny] + cnd) + "\n"
    with open(project_root + "instruments_parsed.csv", "w") as handle:
        handle.write(outchain)


if __name__ == '__main__':
    reparse_instruments()
