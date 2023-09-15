class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "inst"):
            cls.inst = super(Singleton, cls).__new__(cls)
        return cls.inst
