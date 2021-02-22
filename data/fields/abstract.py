import ast
from dataclasses import dataclass

from .fields import FIELDS


def literal_deserializer(string):
    if string is "":
        return None
    try:
        return ast.literal_eval(string)
    except Exception:
        raise Exception("Cannot eval: " + string)


class MetaField(type):
    def __call__(self, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        FIELDS.register_field(instance)
        return instance


class AbstractField(metaclass=MetaField):
    deserializer = None

    def name(self):
        raise NotImplementedError


class AbstractListField(AbstractField):
    deserializer = staticmethod(literal_deserializer)
