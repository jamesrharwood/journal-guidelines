from collections import defaultdict
import itertools


class FieldCollection:
    def __init__(self):
        self._fields = defaultdict(list)

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
