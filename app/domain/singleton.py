from typing import Type


class Singleton(type):
    __instances = {}

    def __call__(cls, *args, **kwargs) -> Type['Singleton']:
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]
