import re


def join_with_or(strings):
    return "|".join(strings)


ALLOWED_TEXTS = [
    "information",
    "instruction",
    "guide",
    "prepar",
    "submis",
    "manuscript",
    "prepar",
    r"author\W*checklist",
    r"checklist\W*for\W*authors",
    r"checklist\W*for\W*contributors",
    r"submission\W*checklist",
    r"manuscript\W*checklist",
    r"journal\W*checklist",
    r"for\W*authors",
    "contributors",
    "requirements",
    "reporting",
    r"article\W*types",
    "polic",
]


def turn_texts_into_regexps(texts):
    if texts and type(texts[0]) == re.Pattern:  # already regular expressions
        return texts
    patterns = [turn_text_into_regex_pattern(text) for text in texts]
    regular_expressions = [
        re.compile(pattern, flags=re.IGNORECASE) for pattern in patterns
    ]
    return regular_expressions


def turn_text_into_regex_pattern(text):
    if text.startswith("^"):
        text = text.replace("^", r"^\s*")
    else:
        text = r".*" + text
    if text.endswith("$"):
        text = text.replace("$", r"\s*$")
    else:
        text += r".*"
    return text
