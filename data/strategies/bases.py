import re

from data.scrape.link_extractors.create_extractor import create_extractor
from data.scrape.utils import clean_url
from .constants import ID


class Strategy:
    def __init__(self, url_pattern, template=None, **extractor_args):
        self.url_pattern = url_pattern.format(ID=ID)
        self.url_regex = re.compile(
            self.url_pattern.replace(".", r"\."), flags=re.IGNORECASE
        )
        self.extractor_args = extractor_args
        self.guideline_url_template = template

    def match_url(self, url):
        url = clean_url(url)
        return self.url_regex.search(url)

    def matches_url(self, url):
        return bool(self.match_url(url))

    def create_link_extractor(self, url):
        return create_extractor(url, allow_domains=[], **self.extractor_args)

    def generate_guideline_urls(self, url, row):
        if self.guideline_url_template is None:
            return []
        match = self.match_url(url)
        urls = [self.guideline_url_template.format(**match.groupdict(), **row)]
        urls = [url for url in urls if url]
        return urls

    def __repr__(self):
        return f"<Strategy: {self.url_pattern}>"
