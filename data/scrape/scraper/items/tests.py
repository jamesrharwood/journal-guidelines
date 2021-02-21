import unittest

from data.scrape.scraper.items import PageData

attr = "EQUATOR_matches"


class TestItem(unittest.TestCase):
    def test_page_data_instance_has_fields(self):
        item = PageData()
        self.assertTrue(item.fields)
        self.assertTrue(attr in item.fields)
