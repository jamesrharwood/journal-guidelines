from .texts_allowed import text_list, join_with_or


def create_link_matcher_string(list_):
    string = join_with_or(text_list)
    string = r"[^/]/[^\?/]*" + f"({string})"
    return string


string = create_link_matcher_string(text_list)
