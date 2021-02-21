from ..rx import RX

dash = RX(
    "dash",
    pattern=r"(—|\-)",
    matches=["-", "—"],
    non_matches=[],
)
