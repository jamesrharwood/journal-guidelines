from .strategies import text_list_from_tag, text_from_tag
from data.fields.abstract import AbstractField


class TextField(AbstractField):
    TYPE = "extracted"
    csv_read_converter = None
    _extraction_strategy = staticmethod(text_from_tag)

    def __init__(self, name, xml_path):
        self.name = name
        self.xml_path = xml_path

    def extract_from_xml(self, xml):
        return self._extraction_strategy(self.xml_path, xml)


class ListField(TextField):
    csv_read_converter = eval
    _extraction_strategy = staticmethod(text_list_from_tag)


FIELDS = [
    TextField("id", "NlmUniqueID"),
    TextField("title", "TitleMain"),
    ListField("languages", "Language"),
    ListField("publisher", "PublicationInfo/Imprint/Entity"),
    ListField("publication_types", "PublicationTypeList/PublicationType"),
    ListField("mesh_headings", "MeshHeadingList/MeshHeading"),
    ListField("urls", "ELocationList/ELocation/ELocationID"),
]
for field in FIELDS:
    field.register()
