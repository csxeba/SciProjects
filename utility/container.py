class Container:

    def __init__(self, *arg, **kw):
        self.__dict__.update({k: None for k in arg})
        self.__dict__.update(kw)

    def __getitem__(self, item):
        if item not in self.__dict__:
            return None
        return self.__dict__[item]

    def __setitem__(self, key, value):
        self.__dict__[key] = value
