TARGETS = []


def iter_targets_by_class(cls):
    return (target for target in TARGETS if isinstance(target, cls))


class TargetMeta(type):
    def __call__(self, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        TARGETS.append(instance)
        return instance


class Target(metaclass=TargetMeta):
    def __init__(self, name, patterns):
        self.name = name
        self.patterns = patterns
        self.fields = [pattern.make_field() for pattern in self.patterns]


from .guidelines import GUIDELINES
from . import equator
