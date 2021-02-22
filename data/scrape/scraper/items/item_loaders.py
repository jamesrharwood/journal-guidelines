from scrapy.loader import ItemLoader

from data.scrape.fields import FIELDS
from data.scrape.utils import get_text_from_xml


class PageDataLoader(ItemLoader):
    @classmethod
    def create(cls, item, response):
        loader = cls(item=item, response=response)
        loader.add_value("id", response.meta["id"])
        loader.add_value("url", response.url)
        loader.add_value("status", response.status)
        loader.context["text"] = get_text_from_xml(response.text.encode("utf-8"))
        for field in FIELDS:
            field.add_to_item_loader(loader)
        return loader