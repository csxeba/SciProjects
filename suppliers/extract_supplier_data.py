import pandas as pd

from SciProjects.suppliers import projectroot, resourceroot


def remove(string, *substr):
    output = string[:]
    for sub in substr:
        output = output.replace(sub, "")
    return output


def parse(string):
    string = str(string)
    beg = string[:4].lower()
    if beg.isdigit() or beg[:2] == "h-" or beg in ("fran", "néme"):
        return "address", string
    if beg == "tel:":
        return "phone", parse_phonenum(string)
    if beg == "fax:":
        return "fax", parse_phonenum(string)
    if beg == "e-ma":
        return "email", parse_email(string)
    return "name", string


def parse_phonenum(string):
    string = remove(string.lower(), "-", "/", "(", ")", " ", "+", ".", ":", "tel", "fax", " ")
    numbers = string.split(",")
    parsed = []
    for num in numbers:
        assert num.isdigit(), f"Not digit: {num} / {numbers}"
        if len(num) == 7:
            num = "361" + string
        elif len(num) == 8:
            num = "36" + string
        if num[:2] == "06":
            num = "36" + string[2:]
        parsed.append("+" + num)
    return ", ".join(parsed)


def parse_email(string):
    string = remove(string.lower(), "-", " ", ":", "email")
    if "," in string:
        string = ", ".join(ss.strip() for ss in string.split(","))
    return string


def main():
    df = pd.read_excel(resourceroot + "supplier_addresses.xlsx")
    col = "name address phone fax email".split()
    suppliers = pd.DataFrame(columns=col)
    current = {c: None for c in col}
    parsing = None
    for row in df["NÉV"]:
        categ, data = parse(row)
        if categ == "name":
            if parsing is not None:
                suppliers = suppliers.append(current, ignore_index=True)
                current = {c: None for c in col}
            parsing = categ
        current[categ] = data
    suppliers.to_excel(projectroot + "suppliers_reparsed.xlsx")


if __name__ == '__main__':
    main()
