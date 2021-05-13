from .publishers import STRATEGIES
from data.fields import FIELDS


def get_strategy_for_url(url):
    for strategy in STRATEGIES:
        if strategy.matches_url(url):
            return strategy


def get_extractor_for_url(url):
    strategy = get_strategy_for_url(url)
    extractor = strategy.create_link_extractor(url) if strategy else None
    return extractor


def get_guideline_urls_for_url(url, row):
    strategy = get_strategy_for_url(url)
    urls = strategy.generate_guideline_urls(url, row)
    return urls


def get_guideline_urls_for_row(row):
    urls = []
    for url in row[FIELDS.urls]:
        urls += get_guideline_urls_for_url(url, row)
    return urls
