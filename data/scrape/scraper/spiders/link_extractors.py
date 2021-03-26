from urllib.parse import urlparse

from scrapy.linkextractors import LinkExtractor
from data.scrape.utils import clean_url


def get_domain_from_url(url):
    return urlparse(url).netloc


def join_link_regexps(*strings):
    string = "|".join(strings)
    string = r"[^/]/[^\?]*" + f"({string})"
    return string


ALLOWED_LINKS = join_link_regexps(
    "information",
    "instruction",
    "guide",
    "prepar",
    "submi",
    "manuscript",
    "prepar",
    "checklist",
)
NOT_ALLOWED_LINKS = join_link_regexps(
    "search",
    "crawl",
    "/doi/",
    "/privacy/",
    "/terms/",
    "template",
    "/librar",
)

ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx", ""]


def create_link_extractor(current_url):
    extractor = LinkExtractor(
        allow=ALLOWED_LINKS,
        deny=NOT_ALLOWED_LINKS,
        allow_domains=get_domain_from_url(current_url),
        process_value=clean_url,
        unique=True,
    )
    extractor.deny_extensions = [
        ext for ext in extractor.deny_extensions if ext not in ALLOWED_EXTENSIONS
    ]
    return extractor
