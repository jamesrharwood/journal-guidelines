from .texts_allowed import ALLOWED_TEXTS, join_with_or


def create_link_matcher_string(list_):
    string = join_with_or(list_)
    string = r"[^/]/[^\?/]*" + f"({string})"
    return string


string = create_link_matcher_string(ALLOWED_TEXTS)
