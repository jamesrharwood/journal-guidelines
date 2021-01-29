# %%
import csv

from collections import namedtuple

from lxml import etree

INFILE = "data/medline_journals.xml"
OUTFILE = "data/medline_journals.csv"


def xml_to_csv():
    nodes = etree.iterparse(INFILE, tag="NLMCatalogRecord")
    fields = fields_to_extract()
    fieldnames = [f.label for f in fields]
    with open(OUTFILE, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for event, node in nodes:
            data = extract_fields_from_node_to_dict(fields, node)
            writer.writerow(data)


def fields_to_extract():
    Field = namedtuple("Field", ("label", "xml_path", "extraction_fn"))
    return [
        Field("id", "NlmUniqueID", text_from_tag),
        Field("title", "TitleMain", text_from_tag),
        Field("language", "Language", text_list_from_tag),
        Field("publisher", "PublicationInfo/Imprint/Entity", text_list_from_tag),
        Field(
            "publication_types",
            "PublicationTypeList/PublicationType",
            text_list_from_tag,
        ),
        Field("mesh_headings", "MeshHeadingList/MeshHeading", text_list_from_tag),
        Field("urls", "ELocationList/ELocation/ELocationID", text_list_from_tag),
    ]


def extract_fields_from_node_to_dict(fields, node):
    return {f.label: f.extraction_fn(f.xml_path, node) for f in fields}


def text_from_tag(tag, tree):
    texts = text_list_from_tag(tag, tree)
    assert len(texts) == 1, f"More than one {tag} tag"
    text = texts[0]
    return text


def text_list_from_tag(tag, tree):
    nodes = tree.iterfind(tag)
    texts = [text_from_node(node) for node in nodes]
    return texts


def text_from_node(node):
    text = " ".join(node.itertext())
    text = text.strip()
    return text


if __name__ == "__main__":
    xml_to_csv()

# %%
