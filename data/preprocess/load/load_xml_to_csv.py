# %%
import csv
from zipfile import ZipFile
from lxml import etree

from .fields import FIELDS


def xml_to_csv(xml_file_path, csv_file_path):
    with ZipFile(xml_file_path) as zip_file:
        xml_file = zip_file.namelist()[0]
        with zip_file.open(xml_file) as infile:
            nodes = etree.iterparse(infile, tag="NLMCatalogRecord")
            write_nodes_to_csv(nodes, csv_file_path)


def write_nodes_to_csv(nodes, csv_file_path):
    fieldnames = [f.name for f in FIELDS]
    with open(csv_file_path, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for event, node in nodes:
            write_node_to_csv(node, writer)


def write_node_to_csv(node, csv_writer):
    data = extract_fields_from_node_to_dict(FIELDS, node)
    csv_writer.writerow(data)


def extract_fields_from_node_to_dict(fields, node):
    return {f.name: f.load_from_xml(node) for f in fields}
