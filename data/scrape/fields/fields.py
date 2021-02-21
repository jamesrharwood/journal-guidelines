from data.fields.abstract import AbstractListField


class ScrapedTextField(AbstractListField):
    output_processor = str

    def __init__(self, regular_expression, name):
        self.name = name
        self.regular_expression = regular_expression

    def add_to_item_loader(self, loader):
        text = loader.context["text"]
        matches = self.regular_expression.finditer(text)
        value = [match.group() for match in matches]
        loader.add_value(self.name, value)


class ScrapedLinkField(ScrapedTextField):
    output_processor = str

    @property
    def _xpath_selector(self):
        pattern = self.regular_expression.pattern
        return f'//body//*[re:match(@href, "{pattern}", "i")]/@href'

    def add_to_item_loader(self, loader):
        loader.add_xpath(self.name, self._xpath_selector)
