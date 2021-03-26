import json
import time
import pathlib
import os


DATADIR = os.path.join(pathlib.Path(__file__).parent.absolute(), "data")


def write_json_to_file(data, filepath):
    with open(filepath, "w") as file_:
        json.dump(data, file_, indent=4)


def load_json_from_file(filepath):
    with open(filepath, "r") as file_:
        return json.load(file_)


def now():
    return time.strftime("%Y%m%d_%H%M%S")


def get_sample_dir_path(name):
    return os.path.join(DATADIR, name)
