import os
from importlib.machinery import SourceFileLoader

from . import Target
from data.scrape.fields.rx import RX, DOMAIN_RX, DEFAULT_FLAGS


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class GuidelineTarget(Target):
    pass

class NonGuidelineTarget(Target):
    pass


class TargetCollection:
    def __init__(self, module_dir, target_class):
        self._module_dir = module_dir
        self._module_file_path = os.path.join(CURRENT_DIR, module_dir)
        self._target_class = target_class
        self._load_guidelines()

    def _make_rx(self, rx_class, name, module):
        return rx_class(
            name,
            module.pattern,
            module.matches,
            module.non_matches,
            getattr(module, "flags", DEFAULT_FLAGS),
        )

    def _make_target(self, name, text_module, domain_module=None):
        patterns = [self._make_rx(RX, name, text_module)]
        if domain_module:
            patterns.append(self._make_rx(DOMAIN_RX, name, domain_module))
        return self._target_class(name, patterns)

    def _ignore_file(self, file_):
        if file_.startswith("_"):
            return True
        if file_.endswith("pyc"):
            return True

    def _load_guidelines(self):
        print("Loading targets from ", self._module_dir)
        for root, dir, files in os.walk(self._module_file_path):
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
                target = self._make_target(
                    name, text_module=text_module, domain_module=domain_module
                )
                setattr(self, name, target)

    def __iter__(self):
        return (getattr(self, x) for x in dir(self) if not x.startswith("_"))


GUIDELINE_TARGETS = TargetCollection('guideline_targets', GuidelineTarget)
NON_GUIDELINE_TARGETS = TargetCollection('non_guideline_targets', NonGuidelineTarget)
