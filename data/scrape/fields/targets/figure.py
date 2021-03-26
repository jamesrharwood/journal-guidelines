from . import GenericTarget as Target
from ..rx import RX

text_rx = RX(
    "manuscript",
    pattern=fr"\bmanuscripts?",
    matches=["manuscript", "manuscripts"],
    non_matches=["manu"],
)


TARGET = Target(
    "manuscript",
    [text_rx],
)
