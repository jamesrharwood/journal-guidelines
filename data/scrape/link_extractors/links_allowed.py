import re

from .texts_allowed import RESTRICTIVE_TEXTS, join_with_or


def create_link_matcher_string(list_):
    string = join_with_or(list_)
    string = r"[^/]/[^\?/]*" + f"({string})"
    return string


string = create_link_matcher_string(RESTRICTIVE_TEXTS)
ALLOWED_LINKS = re.compile(string, flags=re.IGNORECASE)
