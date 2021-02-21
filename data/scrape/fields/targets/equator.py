from . import Target
from ..rx import RX, DOMAIN_RX
from ..common import dash

text_rx = RX(
    "EQUATOR",
    pattern=fr"\bequator([\s{dash}]*network)?",
    matches=[
        "Equator",
        "EQUATOR-Network",
        "EQUATOR Network",
        (" equator", "equator"),
        "EQUATOR — network",
    ],
    non_matches=["network", "Eequator", "-network"],
)

domain_rx = DOMAIN_RX(
    "EQUATOR_domain",
    pattern=r"equator-network\.org",
    matches=[
        "equator-network.org",
        ("www.equator-network.org", 1),
        ("https://www.equator-network.org", 1),
        ("http://equator-network.org/reporting-guidelines/prisma", 1),
        ("equator-network.org something", "equator-network.org"),
    ],
    non_matches=["equator.org"],
)

Target(
    "EQUATOR",
    [text_rx, domain_rx],
)
