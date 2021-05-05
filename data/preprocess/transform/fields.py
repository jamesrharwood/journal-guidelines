import re

from data.fields import FIELDS
from data.fields.abstract import AbstractField, AbstractListField
from data.constants import PIVOT_FROM_COL
from data.scrape.link_extractors.utils import get_root_from_url


class TransformedFieldBase:
    def __init__(self, name, from_field_name, method):
        self.name = name
        self.from_field_name = from_field_name
        self.method = method

    def apply_to_dataframe(self, df):
        return df[self.from_field_name].apply(self.method)


class TransformedField(TransformedFieldBase, AbstractField):
    pass


class TransformedListField(TransformedFieldBase, AbstractListField):
    pass


def include_url(url):
    return not re.search(r"\.(ovid|ncbi)\.", url)


def url_filter(urls):
    return [url for url in urls if include_url(url)]


def is_periodical(types):
    return "Periodical" in types


def is_english(languages):
    return "eng" in languages


def count_publishers(publishers):
    return len(publishers)


def clean_publishers(publishers):
    publishers = [publisher.strip(",") for publisher in publishers]


def get_url_roots(urls):
    return [get_root_from_url(url) for url in urls]


FIELDS = [
    TransformedField(
        "is_periodical",
        FIELDS.publication_types_,
        is_periodical,
    ),
    TransformedField("is_english", FIELDS.languages_, is_english),
    TransformedListField(PIVOT_FROM_COL, FIELDS.urls_raw_, url_filter),
    TransformedListField("publishers_cleaned", FIELDS.publisher_, clean_publishers),
    TransformedListField("url_roots", PIVOT_FROM_COL, get_url_roots),
]
