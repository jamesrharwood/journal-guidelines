from abc import ABC, abstractproperty
from .fields import FIELDS


def abstract_class_property(func):
    return property(classmethod(abstractproperty(func)))


class AbstractField(ABC):
    @abstract_class_property
    def TYPE(self):
        ...

    def register(self):
        FIELDS.register_field(self)
