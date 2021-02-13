from collections import defaultdict
import itertools


class FieldCollection:
    _instance = None

    def __init__(self, fields=[]):
        if self._instance:
            return self._instance
        self._fields = defaultdict(list)
        self.register_fields(fields)
        self._instance = self

    def register_fields(self, fields):
        for field in fields:
            self.register_field(field)

    def register_field(self, field):
        setattr(self, field.name, field)
        setattr(self, field.name + "_", field.name)
        self._fields[field.TYPE].append(field)

    def __iter__(self):
        return itertools.chain.from_iterable(self._fields.values())


FIELDS = FieldCollection()
