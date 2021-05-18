from . import GenericTarget as Target
from ..rx import RX, DOMAIN_RX

text_rx = RX(
    "ICMJE",
    pattern=fr"\b(icmje|International\s*Com+it+e+\s*of\s*Medical\s*Journal\s*Editors)",
    matches=["icmje", "ICMJE", "International committee of medical journal editors"],
    non_matches=["bicmje"],
)

domain_rx = DOMAIN_RX(
    "ICMJE_domain",
    pattern=r"icmje\.org",
    matches=[
        ("http://www/icmje.org", 1),
    ],
    non_matches=["ice.org"],
)


TARGET = Target(
    "ICMJE",
    [text_rx, domain_rx],
)
