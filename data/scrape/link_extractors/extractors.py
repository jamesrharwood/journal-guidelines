from ..utils import clean_url
from .utils import is_service_subdomain, urls_from_same_subdomain, is_pdf
from .constants import TEXT_LENGTH_LIMIT
from .texts_not_allowed import regular_expression as DISALLOWED_TEXTS_REGEX
from .create_extractor import create_link_extractor, create_text_extractor
from data.strategies.strategies import get_extractor_for_url


def extract_links_by_strategy(response):
    extractor = get_extractor_for_url(response.url)
    if not extractor:
        return []
    links = extract_links(response, extractor)
    return links


def extract_links(response, extractor=None):
    is_same_domain = urls_from_same_subdomain(response.url, response.meta["start_url"])
    if not is_same_domain:
        return []
    if is_pdf(response.url):
        return []
    if extractor:
        links = extractor.extract_links(response)
    else:
        links = extract_all_links(response)
    links = filter_links(links)
    links = filter_unique_links(links)
    links = filter_not_visited(links, response)
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
            urls.append(url)
            unique_links.append(link)
    return unique_links


def filter_not_visited(links, response):
    links_to_follow = []
    for link in links:
        cleaned_url = clean_url(link.url)
        if cleaned_url not in response.meta["visited_urls"]:
            links_to_follow.append(link)
    return links_to_follow
