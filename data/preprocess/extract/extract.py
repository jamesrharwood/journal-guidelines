# %%
import csv
import pandas as pd

from zipfile import ZipFile
from lxml import etree

from data.fields import FIELDS
from data.constants import (
    MEDLINE_XML_ZIP_FILE_PATH as IN_FILE_PATH,
    JOURNALS_CSV_FILE_PATH as OUT_FILE_PATH,
)

from data.regular_expressions import rx


def xml_to_csv():
    with ZipFile(IN_FILE_PATH) as zip_file:
        xml_file = zip_file.namelist()[0]
        with zip_file.open(xml_file) as infile:
            nodes = etree.iterparse(infile, tag="NLMCatalogRecord")
            fieldnames = [f.name for f in FIELDS.extracted]
            with open(OUT_FILE_PATH, "w") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for event, node in nodes:
                    data = extract_fields_from_node_to_dict(FIELDS.extracted, node)
                    writer.writerow(data)


def extract_fields_from_node_to_dict(fields, node):
    return {f.name: f.extract_from_xml(node) for f in fields}
