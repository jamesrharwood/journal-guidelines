def preceeded_by(string):
    return r"(?<={})".format(string)


def followed_by(string):
    return r"(?={})".format(string)


def not_preceeded_by(string):
    return r"(?<!{})".format(string)


def not_followed_by(string):
    return r"(?!{})".format(string)
