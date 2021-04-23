import tldextract

from .equivalent_urls import EQUIVALENT_URLS


def urls_from_same_subdomain(url1, url2):
    url1 = get_root_from_url(url1)
    url2 = get_root_from_url(url2)
    if url1 == url2:
        return True
    if EQUIVALENT_URLS.get(url1, None) == url2:
        return True


def get_root_from_url(url):
    # www.sub2.domain.com/page/page -> www.sub2.domain.com
    url = tldextract.extract(url)
    url = ".".join(url)
    url = url.lower()
    return url


def get_domain_from_url(url):
    # www.google.com -> google.com
    parts = tldextract.extract(url)
    return parts.registered_domain


def create_allowed_domains_including_current_url(url):
    domain = get_domain_from_url(url)
    domains = [domain]
    root = get_root_from_url(url)
    equivalent = EQUIVALENT_URLS.get(root, None)
    if equivalent:
        domains.append(equivalent)
    return domains


def is_service_subdomain(url):
    url = tldextract.extract(url)
    if "service" in url[0]:
        return True
