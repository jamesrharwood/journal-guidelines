import re

from .fields import ScrapedLinkField, ScrapedTextField

DEFAULT_FLAGS = re.IGNORECASE


class RX:
    _instances = []
    field_class = ScrapedTextField

    def __init__(
        self,
        name: str,
        pattern: list,
        matches: list,
        non_matches: list,
        flags=DEFAULT_FLAGS,
    ):
        self.name = name
        self.pattern = pattern
        self.matches = matches
        self.non_matches = non_matches
        self.flags = flags
        self.compiled_pattern = re.compile(pattern, flags=flags)
        self._instances.append(self)

    def make_field(self):
        return self.field_class(self.compiled_pattern, self.name + "_matches")

    @property
    def instances(self):
        return self._instances

    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except KeyError:
            return getattr(self.compiled_pattern, name)


class DOMAIN_RX(RX):
    field_class = ScrapedLinkField
