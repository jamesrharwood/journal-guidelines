# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

from data.scrape.fields import FIELDS


def serialize_match_list(lst):
    return [(match.start(), match.stop()) for match in lst]


class PageData(Item):
    id = Field()
    url = Field()
    status = Field()
    link_text = Field()
    char_count = Field()
    word_count = Field()
    origin = Field()
    spider = Field()
    links_of_interest = Field()


for field in FIELDS:
    PageData.fields.update({field.name: Field(output_processor=field.output_processor)})
