import tldextract

from ..fields.targets import TARGETS
from ..fields.rx import DOMAIN_RX


def clean_regex_url(pattern):
    pattern = pattern.replace("\.", ".")
    url = tldextract.extract(pattern)
    url = ".".join([url.domain, url.suffix])
    return url


DENIED_DOMAINS = [
    pattern.pattern
    for target in TARGETS
    for pattern in target.patterns
    if isinstance(pattern, DOMAIN_RX)
]
DENIED_DOMAINS = [clean_regex_url(pattern) for pattern in DENIED_DOMAINS]
DENIED_DOMAINS.extend(
    [
        "elsevier.com/authors",
        "authorservices.wiley.com/",
        "authors.bmj.com/",
        "springer.com/gp/authors-editors",
    ]
)
