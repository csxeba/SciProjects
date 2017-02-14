import time
import string
from abc import ABC, abstractmethod

from geocoder import google


def isdigit(chain, *include):
    digit = True
    for c in chain:
        if c not in tuple(string.digits) + include:
            digit = False
    return digit


class API:

    coder = google

    @staticmethod
    def geocode(addr):
        obj = API.coder(addr)
        if "limit" in obj.status.lower():
            for s in range(3, 0, -1):
                time.sleep(1)
                print("\nQuery limit reached, waiting for API... {}".format(s), end="")

            obj = API.coder(addr)
        if "limit" in obj.status.lower():
            raise RuntimeError("\nQuery limit reached with geocoder API. Exiting!".format())
        return obj.x, obj.y, obj.address


class PlaceType(ABC):
    def __init__(self, rawname):
        self.rawname = rawname
        self.address = None
        self.x = None
        self.y = None
        self.found = None
        if self.reparse():
            self.x = self.y = self.address = "none"

    def geocode(self):
        if self.x or self.y == "none":
            print("\nSkipping invalid address:{}\n".format(self.address))
            return
        if self.x or self.y or self.found:
            print("\nSkipping already geocoded address:{}\n".format(self.address))
            return
        self.x, self.y, self.found = API.geocode(self.address)

    def to_outputline(self):
        return "\t".join((str(self.rawname),
                          str(self.address),
                          str(self.x),
                          str(self.y),
                          str(self.found))) + "\n"

    @abstractmethod
    def reparse(self):
        raise NotImplementedError


class NiceAddress(PlaceType):
    def __init__(self, rawname):
        super().__init__(rawname)

    def reparse(self):
        self.address = "Hungary, " + self.rawname


class KTBT(PlaceType):
    def __init__(self, rawname):
        super().__init__(rawname)

    def reparse(self):
        name = self.rawname\
            .replace(",", " ")\
            .replace("Külterület", "kt")\
            .replace("Belterület", "bt")\
            .replace("HRSZ", "hrsz")\
            .replace("Hrsz", "hrsz")\
            .replace("Km", "km")\
            .replace("KM", "km")\
            .replace("Mol", "mol")\
            .replace("Agip", "agip")\
            .replace("Ipar", "ipar")

        words = [w for w in name.split(" ") if w]
        capitalized = [word for word in words if word[0].lower() != word[0]]
        if len(capitalized) != 1:
            chain = "\n".join("{}: {}".format(i, word) for i, word in enumerate(capitalized))
            chain += "\n-1: Skip"
            chain += "\nKeep these [0] > "
            chosen = input(chain)
            if chosen == "-1":
                return 1
            if not chosen:
                chosen = 0
            capitalized = capitalized[int(chosen)]
        else:
            capitalized = capitalized[0]
        self.address = "Hungary, " + capitalized


class HRSZ(PlaceType):
    def __init__(self, rawname):
        super().__init__(rawname)

    def reparse(self):
        name = self.rawname\
            .replace(":", "")\
            .replace("\\", "")\
            .replace("/", "")\
            .replace("-", "")
        words = [w for w in name.split(" ") if w]
        hrszplace = [i for i, w in enumerate(words) if "hrsz" in w.lower()]
        if len(hrszplace) != 1:
            chain = "\n".join("{}: {}".format(i, word) for i, word in enumerate(words))
            chain += "\n-1: Skip"
            chain += "\nChoose HRSZ > "
            chosen = int(input(chain))
            if chosen == -1:
                return
            hrszplace = chosen
        else:
            hrszplace = hrszplace[0]

        isleftdigit = isdigit(words[hrszplace-1], ".")
        if hrszplace == len(words) - 1:
            isrightdigit = False
        else:
            isrightdigit = isdigit(words[hrszplace + 1], ".")

        dropem = [hrszplace]

        if isleftdigit == isrightdigit:
            chain = "\n".join("{}: {}".format(i, word) for i, word in enumerate(words))
            chain += "\nWhat to drop? Divide by space! > "
            response = input(chain)
            if not response:
                return
            dropem = [int(c) for c in response.split(" ") if c]
        elif isleftdigit:
            dropem.append(hrszplace-1)
        elif isrightdigit:
            dropem.append(hrszplace+1)
        dropem += [i for i, w in enumerate(words) if w.lower() in "ktbtkülterületebelterületetanya"]
        words = (w for i, w in enumerate(words) if i not in dropem)
        self.address = "Hungary, " + ", ".join(words)
