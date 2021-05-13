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

    def matches_url(self, url):
        url = clean_url(url)
        match = self.url_regex.search(url)
        return bool(match)

    def create_link_extractor(self, url):
        return create_extractor(url, allow_domains=[], **self.extractor_args)

    def generate_guideline_urls(self, url, row):
        if self.guideline_url_template is None:
            return []
        match = self.url_regex.search(url)
        id_ = match.groupdict()["id"]
        urls = [self.guideline_url_template.format(ID=id_, **row)]
        urls = [url for url in urls if url]
        return urls

    def __repr__(self):
        return f"<Strategy: {self.url_pattern}>"
