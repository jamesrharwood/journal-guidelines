import unittest
from scrapy.http import HtmlResponse, Request


from data.scrape import link_extractors as le

URL = "https://www.test.com/"
TARGET = "author-guidelines"
DISABLE = False


class Base(unittest.TestCase):
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
        self.assertEqual(
            len(links),
            target,
            f"url: {url}\n\nurls: {urls}\n\nmatched: {[link.url for link in links]}",
        )


class TestLinkExtractors(Base):
    def test_link_extractor_follows(self):
        urls = [
            TARGET,
            "instructions-for-authors",
            TARGET + ".asp",
            TARGET + ".manuscript-composition",
            "wp-content/uploads/2017/01/Manuscript-Cheklist_Original-article.pdf",
        ]
        urls = [URL + url for url in urls]
        self.check_urls_from_url(urls, URL)

    def test_link_extractor_doesnt_follow_author_subdomain(self):
        urls = [
            URL.replace("www", "authors"),
        ]
        self.check_urls_from_url(urls, URL, target=0)

    def test_doesnt_follow(self):
        base = URL + "{}/" + TARGET
        self.check_urls_from_url([base.format("journal")], URL)
        bad_words = [
            "crawl",
            "crawlprevention",
            "doi",
            "article-doi",
            "privacy",
            "template",
            "library",
            "librarians",
            "solutions",
            "legal",
            "transfer",
            "manuscript-transfer",
            "peerreview",
            "peer-reviewers",
            "copyright",
            "figures",
            "figure-formatting",
            "full-text",
            "fulltext",
            "full-article",
            "terms",
            "terms-and-conditions",
            "cookies",
            "information-for-reviewers",
            "login",
            "log-in",
            "crawlprevention/governor?content=%2fjournals%2fpages%2fopen_access%2flicences",
        ]
        urls = [base.format(word) for word in bad_words]
        self.check_urls_from_url(urls, URL, target=0)

    def test_sciencedirect_can_link_to_elsevier(self):
        path = "/journals/ageing-research-reviews/1568-1637/guide-for-authors"
        urls = [
            "https://www.elsevier.com" + path,
            "https://www.sciencedirect.com" + path,
        ]
        url = "http://www.sciencedirect.com/science/journal/15681637"
        extractor = le.extractors.create_link_extractor(url)
        allowed = extractor.allow_domains
        self.assertEqual(len(allowed), 2)
        self.assertTrue("www.elsevier.com" in allowed, allowed)
        self.assertTrue("www.sciencedirect.com" in allowed, allowed)
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
        self.assertFalse(le.utils.urls_from_same_subdomain(start_url, url))
        self.check_urls_from_url(urls, url, target=0, start_url=start_url)

    def test_springer(self):
        urls = ["https://www.springer.com/journal/10544/submission-guidelines"]
        url = "https://link.springer.com/journal/10544/test-not-home-page"
        self.check_urls_from_url(urls, url)

    def test_words_allowed_in_domain_but_not_path(self):
        bad_word = "legal"
        url = URL + TARGET
        self.check_urls_from_url([url], URL)
        url = URL + bad_word + "/" + TARGET
        self.check_urls_from_url([url], URL, target=0)
        url = f"https://www.{bad_word}.com/"
        self.check_urls_from_url([url + TARGET], url)
