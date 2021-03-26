import os

from .utils import load_json_from_file, write_json_to_file, get_sample_dir_path
from data.constants import PREPROCESSED_DATA_FILE_PATH
from data.preprocess.transform.transform import load_csv_to_df

FILENAME = "reference.json"
inputs = {"y": True, "n": False}


def make_reference_file(sample_name):
    ids = load_ids_for_sample_name(sample_name)
    try:
        reference_data = load_reference_data_for_sample_name(sample_name)
    except FileNotFoundError:
        reference_data = []
    ids_already_checked = [datum["id"] for datum in reference_data]
    ids_to_check = [id_ for id_ in ids if id_ not in ids_already_checked]
    df = load_csv_to_df(PREPROCESSED_DATA_FILE_PATH)
    df = df[df.id.isin(ids_to_check)]
    for idx, row in df.iterrows():
        reference_data.append(create_reference(row))
        write_reference_data_for_sample_name(reference_data, sample_name)


def load_ids_for_sample_name(sample_name):
    ids_path = get_sample_ids_filepath(sample_name)
    ids = load_json_from_file(ids_path)
    return ids


def get_sample_ids_filepath(sample_name):
    dirpath = get_sample_dir_path(sample_name)
    return os.path.join(dirpath, "ids.json")


def load_reference_data_for_sample_name(sample_name):
    data_path = get_reference_filepath(sample_name)
    data = load_json_from_file(data_path)
    return data


def create_reference(row):
    url_data = {}
    for url in row["urls"]:
        print(url)
        urls = ask_for_urls(url)
        url_data.update({url: urls})
    return row_to_dict(row, url_data)


def ask_for_urls(url):
    urls = []
    request_url = True
    while request_url is True:
        url = input("url: ").strip()
        if url:
            urls.append(url)
        else:
            request_url = False
    return urls


def row_to_dict(row, url_data):
    return {
        "id": row["id"],
        "title": row["title"],
        "urls": url_data,
    }


def get_reference_filepath(sample_name):
    path = get_sample_dir_path(sample_name)
    return os.path.join(path, FILENAME)


def write_reference_data_for_sample_name(data, sample_name):
    filepath = get_reference_filepath(sample_name)
    write_json_to_file(data, filepath)
