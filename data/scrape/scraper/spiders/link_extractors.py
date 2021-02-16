from urllib.parse import urlparse

from scrapy.linkextractors import LinkExtractor
from data.scrape.utils import clean_url


def get_domain_from_url(url):
    return urlparse(url).netloc


ALLOWED_LINKS = (
    "information",
    "instruction",
    "guide",
    "prepar",
    "submi",
    "manuscript",
    "prepar",
    "checklist",
)
ALLOWED_LINKS = "|".join(ALLOWED_LINKS)
ALLOWED_LINKS = r"[^/]/[^\?]*" + f"({ALLOWED_LINKS})"
NOT_ALLOWED_LINKS = (
    "search",
    "crawl",
    "/doi/",
    "/privacy/",
    "/terms/",
)


def create_link_extractor(current_url):
    return LinkExtractor(
        allow=ALLOWED_LINKS,
        deny=NOT_ALLOWED_LINKS,
        allow_domains=get_domain_from_url(current_url),
        process_value=clean_url,
        unique=True,
    )
