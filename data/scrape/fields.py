from data.fields.abstract import AbstractField
from data.regular_expressions import rx


class ScrapedTextField(AbstractField):
    TYPE = "scraped_text"

    def __init__(self, pattern_name):
        self.name = f"{pattern_name}_matches"
        self.pattern = getattr(rx, pattern_name)


class ScrapedLinkField(AbstractField):
    TYPE = "scraped_link"


TEXT_FIELDS = [ScrapedTextField("equator")]
LINK_FIELDS = [ScrapedLinkField("equator_domain")]

for pattern_name in rx._iter_by_name("guideline"):
    if "domain" in pattern_name:
        field = ScrapedLinkField(pattern_name)
        LINK_FIELDS.append(field)
    else:
        field = ScrapedTextField(pattern_name)
        TEXT_FIELDS.append(field)

for field in LINK_FIELDS:
    field.register()
for field in TEXT_FIELDS:
    field.register()
