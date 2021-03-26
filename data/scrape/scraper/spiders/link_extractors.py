from urllib.parse import urlparse

from scrapy.linkextractors import LinkExtractor
from data.scrape.utils import clean_url


def extract_links(response):
    url_links = link_url_extractor.extract_links(response)
    text_links = link_text_extractor.extract_links(response)
    links = set(url_links + text_links)
    return links


def join_link_regexps(*strings):
    string = join_with_or(*strings)
    string = r"[^/]/[^\?]*" + f"({string})"
    return string


def join_with_or(*strings):
    return "|".join(strings)


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

ALLOWED_TEXT = join_with_or(ALLOWED_LINKS)


link_url_extractor = LinkExtractor(
    allow=ALLOWED_LINKS,
    deny=NOT_ALLOWED_LINKS,
    process_value=clean_url,
    unique=True,
)

link_text_extractor = LinkExtractor(
    restrict_text=ALLOWED_TEXT,
    process_value=clean_url,
    unique=True,
)


def get_domain_from_url(url):
    return urlparse(url).netloc


def create_restricted_link_extractor(current_url):
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
