import os, pkgutil
from importlib.machinery import SourceFileLoader

from ..bases import Strategy

STRATEGIES = []
STRATEGY_DICT = {}

for finder, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
    module = SourceFileLoader(
        module, os.path.join(finder.path, module + ".py")
    ).load_module(module)
    strategy = Strategy(module.url, module.template, **module.extractor_args)
    STRATEGIES.append(strategy)
    STRATEGY_DICT.update({module: strategy})

del strategy, finder, module, SourceFileLoader, os, pkgutil
