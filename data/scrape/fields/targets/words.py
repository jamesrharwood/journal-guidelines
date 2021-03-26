from . import GenericTarget as Target
from ..rx import RX

text_rx = RX(
    "words",
    pattern=fr"\bwords",
    matches=["words"],
    non_matches=["word"],
)


TARGET = Target(
    "word",
    [text_rx],
)
