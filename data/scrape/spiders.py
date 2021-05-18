import logging
import os

from scrapy import Request, Spider
from scrapy.http import TextResponse

from data.scrape.utils import get_bytes_from_pdf
from data.data import BROKEN_LINKS_DIR
from .load_urls import (
    load_generated_guideline_urls_from_csv,
    load_unscraped_urls_df_from_csv,
)
from .link_extractors import extract_links, extract_links_by_strategy
from .utils import clean_url
from .items import PageDataLoader, PageData
from data.constants import INDEX_COL as IDX, PIVOT_TO_COL as URL


class FallbackSpider(Spider):
    name = "fallback"
    journal_urls_df = load_unscraped_urls_df_from_csv()
    start_requests_count = 0

    def start_requests(self):
        requests = [
            Request(
                row[URL],
                callback=self.parse,
                meta={
                    IDX: row[IDX],
                    "visited_urls": [],
                    "link_text": None,
                    "origin": "",
                    "index": idx,
                    "spider": self.name,
                },
                errback=self.errback,
            )
            for idx, row in self.journal_urls_df.iterrows()
        ]
        self.start_requests_count = len(requests)
        return requests

    def parse(self, response):
        print(f"{response.meta['index']}/{self.start_requests_count}", response.url)
        if not response.meta.get("start_url", None):
            response.meta["start_url"] = response.url

        if not hasattr(response, "text"):
            if response.url.endswith(".pdf"):
                body = get_bytes_from_pdf(response)
            else:
                body = b""
            response = response.replace(body=body, cls=TextResponse)

        links = self.extract_links(response)
        response = self.update_response_visited_urls(response, links)
        response.meta["links_of_interest"] = [(link.url, link.text) for link in links]

        page_data_loader = PageDataLoader.create(item=PageData(), response=response)
        yield page_data_loader.load_item()
        requests = self.prepare_requests(links, response)
        for request in requests:
            yield request

    def extract_links(self, response):
        links = extract_links_by_strategy(response)
        if not links:
            links = extract_links(response)
        return links

    def update_response_visited_urls(self, response, links):
        for link in links:
            cleaned_url = clean_url(link.url)
            response.meta["visited_urls"].append(cleaned_url)
        return response

    def prepare_requests(self, links_to_follow, response):
        links_to_return = []
        for link in links_to_follow:
            meta = {k: v for k, v in response.meta.items()}
            meta.update({"link_text": link.text.strip()})
            meta.update({"origin": response.url})
            links_to_return.append(
                Request(link.url, callback=self.parse, meta=meta, errback=self.errback)
            )
        return links_to_return

    def errback(self, failure):
        response = failure.value.response
        fp = os.path.join(BROKEN_LINKS_DIR, f"{response.status}.txt")
        with open(fp, "a") as file_:
            file_.write("\n" + response.url)


class FirstPassSpider(FallbackSpider):
    name = "first_pass"
    journal_urls_df = load_generated_guideline_urls_from_csv()

    def prepare_requests(self, *args, **kwargs):
        return []


class SecondPassSpider(FallbackSpider):
    name = "second_pass"
    journal_urls_df = load_unscraped_urls_df_from_csv()

    def extract_links(self, response):
        links = extract_links_by_strategy(response)
        return links
