import tldextract
import re

from scrapy.linkextractors import LinkExtractor
from data.scrape.utils import clean_url


def extract_links(response):
    is_same_domain = urls_from_same_subdomain(response.url, response.meta["start_url"])
    if not is_same_domain:
        print(response.url, "not same domain as", response.meta["start_url"])
        return []
    # link_url_extractor = create_restricted_link_url_extractor(response.url)
    link_text_extractor = create_restricted_link_text_extractor(response.url)
    url_links = []  # link_url_extractor.extract_links(response)
    text_links = link_text_extractor.extract_links(response)
    links = set(url_links + text_links)
    links = [link for link in links if not is_author_subdomain(link.url)]
    return links


def join_link_regexps(*strings):
    string = join_with_or(*strings)
    string = r"[^/]/[^\?/]*" + f"({string})"
    return string


def join_with_or(*strings):
    return "|".join(strings)


def create_text_regex_list(list_):
    texts = [f".*{text}.*" for text in list_]
    patterns = [re.compile(text, flags=re.IGNORECASE) for text in texts]
    return patterns


TAGS = ["a", "area"]
XPATH = f'//*[{" or ".join(TAGS)} and not(ancestor::footer)]'
ALLOWED_LINKS_RAW = [
    "information",
    "instruction",
    "guide",
    "prepar",
    "submis",
    "manuscript",
    "prepar",
    "checklist",
    "for authors",
    "contribu",
]
ALLOWED_LINKS = join_link_regexps(*ALLOWED_LINKS_RAW)

NOT_ALLOWED_LINKS = join_link_regexps(
    r"\bsearch",
    "crawl",
    "/doi/",
    "/privacy/",
    "/terms",
    "template",
    "/librar",
    "/solutions",
    "legal",
)


ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx", ""]

ALLOWED_TEXT = create_text_regex_list(ALLOWED_LINKS_RAW)
ALLOWED_DOMAINS = [
    "elsevier.com",
    "springer.com",
]

DENIED_DOMAINS = ["equator-network.org"]


def create_restricted_link_url_extractor(current_url):
    extractor = LinkExtractor(
        allow=ALLOWED_LINKS,
        deny=NOT_ALLOWED_LINKS,
        allow_domains=create_allowed_domains_including_current_url(current_url),
        deny_domains=DENIED_DOMAINS,
        process_value=clean_url,
        unique=True,
    )
    extractor.deny_extensions = [
        ext for ext in extractor.deny_extensions if ext not in ALLOWED_EXTENSIONS
    ]
    return extractor


def create_restricted_link_text_extractor(current_url):
    extractor = LinkExtractor(
        restrict_text=ALLOWED_TEXT,
        process_value=clean_url,
        unique=True,
        deny_domains=DENIED_DOMAINS,
        tags=TAGS,
        restrict_xpaths=XPATH,
        allow_domains=create_allowed_domains_including_current_url(current_url),
    )
    extractor.deny_extensions = [
        ext for ext in extractor.deny_extensions if ext not in ALLOWED_EXTENSIONS
    ]
    return extractor


def create_allowed_domains_including_current_url(url):
    domain = get_domain_from_url(url)
    domains = [domain for domain in ALLOWED_DOMAINS]
    domains.append(domain)
    return domains


def get_domain_from_url(url):
    parts = tldextract.extract(url)
    return parts.registered_domain


def urls_from_same_subdomain(url1, url2):
    url1 = extract_subdomain(url1)
    url2 = extract_subdomain(url2)
    return url1 == url2


def extract_subdomain(url):
    url = tldextract.extract(url)
    url = ".".join(url)
    url = url.lower()
    return url


def is_author_subdomain(url):
    if "service.elsevier" in url:
        return True
    url = tldextract.extract(url)
    return "author" in url[0]
