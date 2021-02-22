from data.fields.abstract import AbstractField
from data.scrape.fields.targets import TARGETS, GUIDELINE_TARGETS, EQUATOR_TARGET


class HasAny(AbstractField):
    def __init__(self, name, field_names):
        self.name = name
        self.field_names = field_names

    def apply_to_dataframe(self, df):
        df[self.name] = df.apply(self.has_any, axis=1)

    def has_any(self, df):
        return any([df[name] for name in self.field_names])


POSTPROCESSED_FIELDS = [
    HasAny(target.name, [field.name for field in target.fields]) for target in TARGETS
]

HAS_EQUATOR = HasAny("EQUATOR", [field.name for field in EQUATOR_TARGET.fields])

HAS_ANY_GUIDELINES = HasAny(
    "Guidelines",
    [field.name for target in GUIDELINE_TARGETS for field in target.fields],
)

POSTPROCESSED_FIELDS.append(HAS_EQUATOR)
POSTPROCESSED_FIELDS.append(HAS_ANY_GUIDELINES)
