import re


def join_with_or(strings):
    return "|".join(strings)


SPACE = r"\W*"

INFORMATION = r"info(rmation)?"
PREPARATION = r"prep((a|e)r(e|ation))?"
AUTHOR = r"(author|contributor|researcher)s?"
MANUSCRIPT = r"(manuscript|{PREPARATION}|article|submission|reporting)"
GUIDELINES_OR_INFORMATION = (
    fr"(guide(line)?|chec?klist|instruction|{INFORMATION}|requirement|{PREPARATION})s?"
)
GUIDELINES = GUIDELINES_OR_INFORMATION.replace(f"|{INFORMATION}", "")

AUTHOR_GUIDELINES = AUTHOR + SPACE + GUIDELINES_OR_INFORMATION
GUIDELINES_FOR_AUTHORS = GUIDELINES_OR_INFORMATION + SPACE + "for" + SPACE + AUTHOR
MANUSCRIPT_GUIDELINES = MANUSCRIPT + SPACE + GUIDELINES_OR_INFORMATION
GUIDELINES_FOR_MANUSCRIPTS = (
    GUIDELINES_OR_INFORMATION + SPACE + "for" + SPACE + MANUSCRIPT
)
AUTHOR_AT_END = "authors?[^/]*$"


RESTRICTIVE_TEXTS = [
    AUTHOR_GUIDELINES,
    GUIDELINES_FOR_AUTHORS,
    GUIDELINES_FOR_MANUSCRIPTS,
    MANUSCRIPT_GUIDELINES,
    r"/\W*" + GUIDELINES,
    AUTHOR_AT_END,
]

NON_RESTRICTIVE_TEXTS = RESTRICTIVE_TEXTS + [
    f"journal{SPACE}{GUIDELINES}",
    f"article{SPACE}types",
    f"prepare{SPACE}your{SPACE}manuscript",
    r"^\W*" + GUIDELINES,
]

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


NON_RESTRICTIVE_TEXTS_REGEXS = turn_texts_into_regexps(NON_RESTRICTIVE_TEXTS)
