from scrapy.linkextractors import LinkExtractor
from ..utils import clean_url
from .utils import (
    is_service_subdomain,
    create_allowed_domains_including_current_url,
    urls_from_same_subdomain,
)
from .constants import TEXT_LENGTH_LIMIT
from .texts_not_allowed import regular_expression as DISALLOWED_TEXTS_REGEX
from .texts_allowed import regular_expressions as ALLOWED_TEXT
from .domains_not_allowed import DENIED_DOMAINS
from .links_allowed import string as ALLOWED_LINKS
from .links_not_allowed import string as NOT_ALLOWED_LINKS


TAGS = ["a", "area"]
XPATH = f'//*[{" or ".join(TAGS)} and not(ancestor::footer)]'
ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx", "", ".asp"]

KWARGS = dict(
    deny=NOT_ALLOWED_LINKS,
    deny_domains=DENIED_DOMAINS,
    unique=False,
    tags=TAGS,
    restrict_xpaths=XPATH,
)


def extract_links(response):
    is_same_domain = urls_from_same_subdomain(response.url, response.meta["start_url"])
    if not is_same_domain:
        return []
    links = extract_all_links(response)
    links = filter_links(links)
    links = filter_unique_links(links)
    return links


def extract_all_links(response):
    url = response.url
    links_by_url = create_link_extractor(url).extract_links(response)
    links_by_text = create_text_extractor(url).extract_links(response)
    return set(links_by_url + links_by_text)


def filter_links(links):
    links = [link for link in links if not is_service_subdomain(link.url)]
    links = [link for link in links if len(link.text.strip()) <= TEXT_LENGTH_LIMIT]
    links = [link for link in links if not DISALLOWED_TEXTS_REGEX.search(link.text)]
    return links


def filter_unique_links(links):
    urls = []
    unique_links = []
    for link in links:
        url = clean_url(link.url)
        if url not in urls:
            urls.append(link.url)
            unique_links.append(link)
    return unique_links


def create_link_extractor(url):
    return create_extractor(url, allow=ALLOWED_LINKS)


def create_text_extractor(url):
    return create_extractor(url, restrict_text=ALLOWED_TEXT)


def create_extractor(url, **kwargs):
    extractor = LinkExtractor(
        **kwargs,
        **KWARGS,
        allow_domains=create_allowed_domains_including_current_url(url),
    )
    extractor.deny_extensions = [
        ext for ext in extractor.deny_extensions if ext not in ALLOWED_EXTENSIONS
    ]
    return extractor
