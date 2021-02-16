# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

from data.scrape.fields import TEXT_FIELDS, LINK_FIELDS


def serialize_match_list(lst):
    return [(match.start(), match.stop()) for match in lst]


class PageData(Item):
    id = Field()
    url = Field()
    status = Field()


for field in TEXT_FIELDS:
    setattr(
        PageData,
        field.name,
        Field(serializer=serialize_match_list),
    )
    setattr(PageData, field.name, Field())
