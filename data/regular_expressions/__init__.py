# A convenient module for defining regular expressions alongside their tests
# To add a new regular expression, add a file to /patterns. It must include a pattern, a list of
# strings to match (or tuples for partial matches), and a list of string that shouldn't match.
# Can also include flags, optionally. Combine flags using | e.g. flags = re.I|re.M

import os
import re
from importlib.machinery import SourceFileLoader
from collections import defaultdict


PATTERN_DIR = "patterns/"
PATTERN_PATH = os.path.join(__path__[0], PATTERN_DIR)


class RegularExpressions(object):
    def __init__(self):
        self._tags = defaultdict(list)
        for module in self._pattern_module_import_iterator():
            self._register_module(module)

    def _register_module(self, module):
        flags = getattr(module, "flags", re.IGNORECASE)
        rx = re.compile(module.pattern, flags)
        setattr(self, module.name, rx)

    def _pattern_module_import_iterator(self):
        for root, dirs, files in os.walk(PATTERN_PATH):
            for file_ in files:
                if self._ignore_file(file_):
                    continue
                file_path = os.path.join(root, file_)
                module = SourceFileLoader(file_, file_path)
                module = module.load_module(file_)
                module.name = (
                    file_path.replace(PATTERN_PATH, "")
                    .strip("/")
                    .replace("/", "_")
                    .split(".")[0]
                )
                yield module

    def _iter_by_name(self, *args):
        for pattern in self:
            substrings = pattern.split("_")
            if all(arg in substrings for arg in args):
                yield pattern

    def _ignore_file(self, file_):
        if file_.startswith("_"):
            return True
        if file_.endswith("pyc"):
            return True

    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith("_"):
                yield attr


rx = RegularExpressions()
