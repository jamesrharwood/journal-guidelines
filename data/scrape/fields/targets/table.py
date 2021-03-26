from . import GenericTarget as Target
from ..rx import RX

text_rx = RX(
    "table",
    pattern=fr"\btables?",
    matches=["table", "tables"],
    non_matches=["tabulate"],
)


TARGET = Target(
    "table",
    [text_rx],
)
