from .strategies import text_list_from_tag, text_from_tag
from data.fields.abstract import AbstractField, AbstractListField
from data.constants import INDEX_COL


class LoadedFieldBase:
    def __init__(self, name, xml_path):
        self.name = name
        self.xml_path = xml_path

    def load_from_xml(self, xml):
        return self._extraction_strategy(self.xml_path, xml)


class TextField(LoadedFieldBase, AbstractField):
    _extraction_strategy = staticmethod(text_from_tag)


class ListField(LoadedFieldBase, AbstractListField):
    _extraction_strategy = staticmethod(text_list_from_tag)


LANGUAGES_COL_NAME = "languages"
PUBLICATION_TYPES_COL_NAME = "publication_types"
URLS_RAW_COL_NAME = "urls_raw"
ISSNS_PRINT_COL_NAME = "issns_print"
ISSNS_ELECTRONIC_COL_NAME = "issns_electronic"

FIELDS = [
    TextField(INDEX_COL, "NlmUniqueID"),
    TextField("title", "TitleMain"),
    ListField(LANGUAGES_COL_NAME, "Language"),
    ListField("publishers_raw", "PublicationInfo/Imprint/Entity"),
    ListField(PUBLICATION_TYPES_COL_NAME, "PublicationTypeList/PublicationType"),
    ListField("mesh_headings", "MeshHeadingList/MeshHeading"),
    ListField(URLS_RAW_COL_NAME, "ELocationList/ELocation/ELocationID"),
    ListField(ISSNS_PRINT_COL_NAME, "ISSN[@IssnType='Print']"),
    ListField(ISSNS_ELECTRONIC_COL_NAME, "ISSN[@IssnType='Electronic']"),
]
