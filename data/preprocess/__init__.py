from .load import xml_to_csv
from .transform import transform


def preprocess(xml_zip_file_path, csv_file_path):
    xml_to_csv(xml_zip_file_path, csv_file_path)
    transform(csv_file_path)
