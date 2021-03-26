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


class GenericTarget(Target):
    pass


from .guidelines import GUIDELINE_TARGETS
from .equator import EQUATOR_TARGET
from .icmje import TARGET
from .section import TARGET
from .manuscript import TARGET
from .table import TARGET
from .words import TARGET
