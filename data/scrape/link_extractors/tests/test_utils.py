import unittest

from ..utils import get_domain_from_url, get_root_from_url


class TestUtils(unittest.TestCase):
    def test_get_root(self):
        for url, target in [
            ("http://www.test.com", "www.test.com"),
            ("https://www.sub2.domain.com", "www.sub2.domain.com"),
            ("http://www.test.com/path/page", "www.test.com"),
            ("https://test.com", "test.com"),
        ]:
            self.assertEqual(target, get_root_from_url(url))

    def test_get_domain(self):
        for url, target in [
            ("https://www.test.com", "test.com"),
            ("http://www.sub2.test.com", "test.com"),
            ("https://www.test.com/path/page", "test.com"),
        ]:
            self.assertEqual(target, get_domain_from_url(url))
