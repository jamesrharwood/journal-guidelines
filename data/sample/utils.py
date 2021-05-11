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


class Timer:
    """
    Context manager as a python timer
    """

    def __init__(self):
        self.start = None

    def __enter__(self):
        """
        Notes the time at the start of the iteration
        """
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Prints the time taken at the end of the iteration
        """
        print("Time to finish the task: ", time.time() - self.start)


def get_filepath_for_sample_and_feed(sample_name, feed_name):
    dirpath = get_sample_dir_path(sample_name)
    return os.path.join(dirpath, feed_name)
