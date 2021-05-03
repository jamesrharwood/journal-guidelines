from unittest import TestCase

from data.scrape.link_extractors.utils import urls_from_same_subdomain as fn


class TestUrlsSubdomains(TestCase):
    def test_same_domain(self):
        url = "https://www.test.com/"
        self.assertTrue(fn(url, url + "page"))

    def test_same_domain_paths(self):
        self.assertTrue(fn("www.t.com", "www.t.com/path"))

    def test_same_domain_http(self):
        self.assertTrue(fn("http://www.t.com", "https://www.t.com"))

    def test_different_domain(self):
        self.assertFalse(fn("https://www.test.com", "https://app.test.com"))
