from unittest import TestCase
from scrapy.http import HtmlResponse, Request


from data.scrape import link_extractors as le

URL = "https://www.test.com/"
TARGET = "author-guidelines"
DISABLE = True


class TestLinkExtractors(TestCase):
    def test_get_domain(self):
        data = [
            ("https://www.test.com", "test.com"),
            ("https://subdomain.domain.co.uk/path/to/page", "domain.co.uk"),
        ]
        for url, target in data:
            self.assertEqual(le.get_domain_from_url(url), target)

    def test_link_extractor_follows(self):
        urls = [
            TARGET,
            "instructions-for-authors",
            TARGET + ".asp",
            TARGET + ".manuscript-composition",
        ]
        urls = [URL + url for url in urls]
        self.check_urls_from_url(urls, URL)

    def test_link_extractor_doesnt_follow(self):
        urls = [URL.replace("www", "authors")]
        self.check_urls_from_url(urls, URL, target=0)

    def test_sciencedirect_can_link_to_elsevier(self):
        path = "/journals/ageing-research-reviews/1568-1637/guide-for-authors"
        urls = [
            "https://www.elsevier.com" + path,
            "https://www.sciencedirect.com" + path,
        ]
        url = "http://www.sciencedirect.com/science/journal/15681637"
        extractor = le.create_restricted_link_url_extractor(url)
        self.assertEqual(len(extractor.allow_domains), 3)
        self.check_urls_from_url(urls, url)

    def test_urls_with_search_in_not_followed(self):
        urls = [URL + TARGET]
        self.check_urls_from_url(urls, URL)
        urls = [URL + "search"]
        self.check_urls_from_url(urls, URL, target=0)
        urls = [URL + "research-" + TARGET]
        self.check_urls_from_url(urls, URL)

    def test_crawl_prevention_not_followed(self):
        urls = [URL + "crawlprevention-author-guidelines"]
        self.check_urls_from_url(urls, URL, target=0)

    def test_urls_not_extracted_if_on_different_subdomain(self):
        start_url = "https://www.start.com"
        url = "https://www.test.com"
        urls = ["https://www.test.com/author-guidelines"]
        self.assertFalse(le.urls_from_same_subdomain(start_url, url))
        self.check_urls_from_url(urls, url, target=0, start_url=start_url)

    def check_urls_from_url(self, urls, url, target=None, start_url=None):
        html = [f'<a href="{url}""></a>' for url in urls]
        html = "".join(html)
        html = f"<body>{html}</body>"
        request = Request(url, meta={"start_url": start_url or url})
        response = HtmlResponse(url=url, body=html, encoding="utf-8", request=request)
        links = le.extract_links(response)
        if target is None:
            target = len(urls)
        target = 0 if DISABLE else target
        self.assertEqual(len(links), target, f"{url}: {urls}")

    def test_springer(self):
        urls = ["https://www.springer.com/journal/10544/submission-guidelines"]
        url = "https://link.springer.com/journal/10544"
        self.check_urls_from_url(urls, url)
