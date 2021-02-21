class FieldCollection:
    def __init__(self):
        self._fields = []

    def register_fields(self, fields):
        for field in fields:
            self.register_field(field)

    def register_field(self, field):
        setattr(self, field.name, field)
        setattr(self, field.name + "_", field.name)
        self._fields.append(field)

    def iter_by_class(self, cls):
        return (field for field in self._fields if isinstance(field, cls))

    def __iter__(self):
        return (field for field in self._fields)


FIELDS = FieldCollection()
