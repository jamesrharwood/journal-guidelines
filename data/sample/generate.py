import os

from random import randint

from data.preprocess.transform.transform import load_csv_to_df
from data.constants import PREPROCESSED_DATA_FILE_PATH
from .utils import now, write_json_to_file, get_sample_dir_path

SAMPLE_IDS_FILENAME = "ids.json"


def generate_sample(size=100, name=None):
    name = name or now()
    path = make_sample_filepath(name)
    df = load_csv_to_df(PREPROCESSED_DATA_FILE_PATH)
    max_ = len(df.index)
    locs = [randint(0, max_ - 1) for x in range(size)]
    df = df.iloc[locs]
    write_json_to_file(list(df["id"]), path)


def make_sample_filepath(name):
    dirpath = get_sample_dir_path(name)
    os.mkdir(dirpath)
    filepath = get_sample_ids_filepath(name)
    return filepath


def get_sample_ids_filepath(name):
    dirpath = get_sample_dir_path(name)
    return os.path.join(dirpath, SAMPLE_IDS_FILENAME)
