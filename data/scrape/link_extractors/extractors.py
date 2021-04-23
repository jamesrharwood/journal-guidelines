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


def extract_links(response):
    is_same_domain = urls_from_same_subdomain(response.url, response.meta["start_url"])
    if not is_same_domain:
        #    print(response.url, "not same domain as", response.meta["start_url"])
        return []
    # link_url_extractor = create_restricted_link_url_extractor(response.url)
    link_text_extractor = create_restricted_link_text_extractor(response.url)
    url_links = []  # link_url_extractor.extract_links(response)
    text_links = link_text_extractor.extract_links(response)
    links = set(url_links + text_links)
    links = [link for link in links if not is_service_subdomain(link.url)]
    links = [link for link in links if len(link.text.strip()) <= TEXT_LENGTH_LIMIT]
    links = [link for link in links if not DISALLOWED_TEXTS_REGEX.search(link.text)]
    urls = []
    unique_links = []
    for link in links:
        url = clean_url(link.url)
        if url not in urls:
            urls.append(link.url)
            unique_links.append(link)
    return unique_links


TAGS = ["a", "area"]
XPATH = f'//*[{" or ".join(TAGS)} and not(ancestor::footer)]'
ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx", "", ".asp"]


def create_restricted_link_url_extractor(current_url):
    extractor = LinkExtractor(
        allow=ALLOWED_LINKS,
        deny=NOT_ALLOWED_LINKS,
        allow_domains=create_allowed_domains_including_current_url(current_url),
        deny_domains=DENIED_DOMAINS,
        unique=False,
    )
    extractor.deny_extensions = [
        ext for ext in extractor.deny_extensions if ext not in ALLOWED_EXTENSIONS
    ]
    return extractor


def create_restricted_link_text_extractor(current_url):
    extractor = LinkExtractor(
        restrict_text=ALLOWED_TEXT,
        deny=NOT_ALLOWED_LINKS,
        # process_value=clean_url,
        unique=False,
        deny_domains=DENIED_DOMAINS,
        tags=TAGS,
        restrict_xpaths=XPATH,
        allow_domains=create_allowed_domains_including_current_url(current_url),
    )
    extractor.deny_extensions = [
        ext for ext in extractor.deny_extensions if ext not in ALLOWED_EXTENSIONS
    ]
    return extractor
