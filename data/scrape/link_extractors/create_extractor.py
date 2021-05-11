from scrapy.linkextractors import LinkExtractor

from .texts_allowed import (
    NON_RESTRICTIVE_TEXTS_REGEXS,
    turn_texts_into_regexps,
)
from .links_not_allowed import string as NOT_ALLOWED_LINKS
from .links_allowed import ALLOWED_LINKS
from .utils import create_allowed_domains_including_current_url


TAGS = ("a", "area")
XPATH = "//*[(self::a or self::area) and not(ancestor-or-self::footer)]"
ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx", "", ".asp"]
KWARGS = dict(
    deny=NOT_ALLOWED_LINKS,
    unique=False,
    tags=TAGS,
    restrict_xpaths=XPATH,
)


def create_link_extractor(url):
    return create_extractor(url, allow=ALLOWED_LINKS)


def create_text_extractor(url):
    return create_extractor(url, restrict_text=NON_RESTRICTIVE_TEXTS_REGEXS)


def create_extractor(url, **kwargs):
    restrict_text = kwargs.pop("restrict_text", [])
    restrict_text = turn_texts_into_regexps(restrict_text)
    allow_domains = kwargs.pop(
        "allow_domains", create_allowed_domains_including_current_url(url)
    )
    extractor = LinkExtractor(
        **kwargs,
        **KWARGS,
        restrict_text=restrict_text,
        allow_domains=allow_domains,
    )
    extractor.deny_extensions = [
        ext for ext in extractor.deny_extensions if ext not in ALLOWED_EXTENSIONS
    ]
    return extractor
