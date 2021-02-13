# A convenient module for defining regular expressions alongside their tests
# To add a new regular expression, add a file to /patterns. It must include a pattern, a list of
# strings to match (or tuples for partial matches), and a list of string that shouldn't match.
# Can also include flags, optionally. Combine flags using | e.g. flags = re.I|re.M

import os
from importlib.machinery import SourceFileLoader
import re


class RegularExpressions(object):
    def __init__(self):
        for module in self._pattern_module_import_iterator():
            self._register_module(module)

    def _register_module(self, module):
        flags = getattr(module, "flags", 0)
        rx = re.compile(module.pattern, flags)
        assert not hasattr(self, module.name)
        setattr(self, module.name, rx)

    def _pattern_module_import_iterator(self):
        path = os.path.join(__path__[0], "patterns")
        for root, dirs, files in os.walk(path):
            for file_ in files:
                if self._ignore_file(file_):
                    continue
                module = SourceFileLoader(file_, os.path.join(root, file_))
                module = module.load_module(file_)
                module.name = file_.split(".")[0]
                yield module

    def _ignore_file(self, file_):
        if file_.startswith("_"):
            return True
        if file_.endswith("pyc"):
            return True


rx = RegularExpressions()
