import tldextract

from ..fields.targets import TARGETS
from ..fields.rx import DOMAIN_RX


DENIED_DOMAINS = [
    pattern
    for target in TARGETS
    for pattern in target.patterns
    if isinstance(pattern, DOMAIN_RX)
]
DENIED_DOMAINS = [pattern.sub(r"\\", "") for pattern in DENIED_DOMAINS]
DENIED_DOMAINS = [tldextract.extract(url) for url in DENIED_DOMAINS]
DENIED_DOMAINS = ["".join([url.domain, url.suffix]) for url in DENIED_DOMAINS]
DENIED_DOMAINS.extend(
    [
        "elsevier.com/authors",
    ]
)
