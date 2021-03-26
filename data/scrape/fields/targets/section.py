from . import GenericTarget as Target
from ..rx import RX

text_rx = RX(
    "section",
    pattern=fr"\bsections?\b",
    matches=["section", "sections"],
    non_matches=["sectioned"],
)


TARGET = Target(
    "section",
    [text_rx],
)
