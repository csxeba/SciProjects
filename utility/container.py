class Container:

    def __init__(self, *arg, **kw):
        self.__dict__.update({k: None for k in arg})
        self.__dict__.update(kw)

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value):
        self.__dict__[key] = value
