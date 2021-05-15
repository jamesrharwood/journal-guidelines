import re

from data.fields import FIELDS
from data.fields.abstract import AbstractField, AbstractListField
from data.constants import PIVOT_FROM_COL
from data.scrape.link_extractors.utils import get_root_from_url, get_domain_from_url
from data.strategies.strategies import get_guideline_urls_for_row


class TransformedFieldBase:
    def __init__(self, name, from_field_name, method):
        self.name = name
        self.from_field_name = from_field_name
        self.method = method

    def apply_to_dataframe(self, df):
        if self.from_field_name:
            return df[self.from_field_name].apply(self.method)
        else:
            return df.apply(self.method, axis=1)


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
    publishers = [publisher.strip(", ") for publisher in publishers]
    return publishers


def get_url_roots(urls):
    return [get_root_from_url(url) for url in urls]


def get_url_domains(urls):
    return [get_domain_from_url(url) for url in urls]


def include(row):
    if row["is_english"] is True:
        if row["is_periodical"] is True:
            if bool(row["urls"]) is True:
                return True
    return False


def get_first(list_):
    if list_:
        return list_[0]
    return None


FIELDS = [
    TransformedField(
        "is_periodical",
        FIELDS.publication_types_,
        is_periodical,
    ),
    TransformedField("is_english", FIELDS.languages_, is_english),
    TransformedListField(PIVOT_FROM_COL, FIELDS.urls_raw_, url_filter),
    TransformedListField("publishers", FIELDS.publishers_raw_, clean_publishers),
    TransformedListField("url_roots", PIVOT_FROM_COL, get_url_roots),
    TransformedListField("url_domains", PIVOT_FROM_COL, get_url_domains),
    TransformedField("issn_electronic", FIELDS.issns_electronic_, get_first),
    TransformedField("issn_print", FIELDS.issns_print_, get_first),
    TransformedListField(
        "urls_generated_guideline_pages", None, get_guideline_urls_for_row
    ),
    TransformedField("include", None, include),
]
