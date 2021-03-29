from scrapy.loader import ItemLoader

from data.scrape.fields import FIELDS
from data.scrape.utils import get_text_from_response


class PageDataLoader(ItemLoader):
    @classmethod
    def create(cls, item, response):
        loader = cls(item=item, response=response)
        loader.add_value("id", response.meta["id"])
        loader.add_value("url", response.url)
        loader.add_value("status", response.status)
        loader.add_value("link_text", response.meta.get("link_text", None))
        loader.context["text"] = get_text_from_response(response)
        for field in FIELDS:
            field.add_to_item_loader(loader)
        return loader
