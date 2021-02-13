import re

from data.fields import FIELDS
from data.fields.abstract import AbstractField


class TransformedField(AbstractField):
    TYPE = "transformed"

    def __init__(self, name, from_field_name, method):
        self.name = name
        self.from_field_name = from_field_name
        self.method = method

    def apply_to_dataframe(self, df):
        return df[self.from_field_name].apply(self.method)


def include_url(url):
    return not re.search(r"\.(ovid|ncbi)\.", url)


def url_filter(urls):
    return [url for url in urls if include_url(url)]


def is_periodical(types):
    return "Periodical" in types


def is_english(languages):
    return "eng" in languages


FIELDS = [
    TransformedField(
        "is_periodical",
        FIELDS.publication_types,
        is_periodical,
    ),
    TransformedField("is_english", FIELDS.languages, is_english),
    TransformedField("urls_filtered", FIELDS.urls, url_filter),
]
for field in FIELDS:
    field.register()
