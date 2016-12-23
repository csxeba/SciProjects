import time

OUTFLPATH = "outfl.csv"


def parse_addresses(addresses, parser):

    def get_parser():
        if parser == "arcgis":
            from geocoder import arcgis as api
        elif parser == "google":
            from geocoder import google as api
        else:
            raise RuntimeError("(Yet) Unsupported parser!")
        return api

    def get_output_file_handle():
        import os
        handle = open(OUTFLPATH, "a", encoding="utf8")
        if os.path.exists(OUTFLPATH):
            if os.stat(OUTFLPATH).st_size == 0:
                header = "CIM\tX\tY\tFOUND\tAPI\n"
                handle.write(header)
        return handle

    def adjust_address_string(adr):
        if not adr:
            print("Empty address string! Skipped {}!".format(i))
            return ""
        return "Hungary, " + adr

    def pull_data_from_api(api, adr):
        obj = api(adr)
        if "limit" in obj.status.lower():
            for s in range(3, 0, -1):
                time.sleep(1)
                print("\rQuery limit reached, waiting for API... {}".format(s), end="")

            obj = api(adr)
        if "limit" in obj.status.lower():
            raise RuntimeError("Query limit reached with {}. Exiting!".format(parser))

        return adr, obj.x, obj.y, obj.address

    def append_current_line_to_file(adr, x, y, hit):
        line = "\t".join([str(adr), str(x), str(y), str(hit), parser])
        line += "\n"
        output.write(line)

    print("Parsing with", parser)
    geocoder_api = get_parser()

    output = get_output_file_handle()

    skips = 0
    n = len(addresses)
    for i, address in enumerate(addresses):
        print("\r{}/{} ".format(i+1, n), end=" ")

        address = adjust_address_string(address)
        data = pull_data_from_api(geocoder_api, address)
        append_current_line_to_file(*data)

    print()
    print("PARSING DONE!")
    print("STAT:")
    print("SKIPS:", skips, "/", n, "({}%)".format(int(100*skips/n)))
    output.close()


if __name__ == '__main__':
    address_chain = open("D:/Project_MobilGeo/03tapogatozas.csv",
                         "r", encoding="utf8").read()
    address_list = list(set(address_chain.split("\n")))

    parse_addresses(address_list, parser="google")

    print("Finite Incantatum!")
