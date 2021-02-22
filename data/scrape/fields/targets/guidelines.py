import os
from importlib.machinery import SourceFileLoader

from . import Target
from data.scrape.fields.rx import RX, DOMAIN_RX, DEFAULT_FLAGS


MODULE_DIR = "guideline_modules"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODULE_FILE_PATH = os.path.join(CURRENT_DIR, MODULE_DIR)


class GuidelineTarget(Target):
    pass


class GuidelineTargets:
    def __init__(self):
        self._load_guidelines()

    def _make_rx(self, rx_class, name, module):
        return rx_class(
            name,
            module.pattern,
            module.matches,
            module.non_matches,
            getattr(module, "flags", DEFAULT_FLAGS),
        )

    def _make_guideline(self, name, text_module, domain_module=None):
        patterns = [self._make_rx(RX, name, text_module)]
        if domain_module:
            patterns.append(self._make_rx(DOMAIN_RX, name, domain_module))
        return GuidelineTarget(name, patterns)

    def _ignore_file(self, file_):
        if file_.startswith("_"):
            return True
        if file_.endswith("pyc"):
            return True

    def _load_guidelines(self):
        print("Loading guidelines from ", MODULE_FILE_PATH)
        for root, dir, files in os.walk(MODULE_FILE_PATH):
            if root.endswith("_"):
                continue
            name = root.split("/")[-1]
            text_module = None
            domain_module = None
            for file_ in files:
                if self._ignore_file(file_):
                    continue
                file_path = os.path.join(root, file_)
                module = SourceFileLoader(file_, file_path)
                module = module.load_module(file_)
                if "domain" in file_:
                    domain_module = module
                else:
                    assert text_module is None
                    text_module = module
            if text_module:
                guideline = self._make_guideline(
                    name, text_module=text_module, domain_module=domain_module
                )
                setattr(self, name, guideline)

    def __iter__(self):
        return (getattr(self, x) for x in dir(self) if not x.startswith("_"))


GUIDELINE_TARGETS = GuidelineTargets()
