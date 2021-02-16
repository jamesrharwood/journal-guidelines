from scrapy.loader import ItemLoader

from data.scrape.fields import TEXT_FIELDS, LINK_FIELDS
from data.scrape.utils import get_text_from_xml


def make_link_selector(pattern):
    return f'//body//*[re:match(@href, "{pattern}", "i")]'


class PageDataLoader(ItemLoader):
    @classmethod
    def create(cls, item, response):
        loader = cls(item=item, response=response)
        loader.add_value("id", response.meta["id"])
        loader.add_value("url", response.url)
        loader.add_value("status", response.status)
        text = get_text_from_xml(response.body.encode("utf-8"))
        for field in TEXT_FIELDS:
            loader.add_value(field.name, field.pattern.finditer(text))
        for field in LINK_FIELDS:
            loader.add_xpath(field.name, make_link_selector(field.pattern.pattern))
        return loader
