def before(string):
    return r"(?<={})".format(string)


def after(string):
    return r"(?={})".format(string)


def not_before(string):
    return r"(?<!{})".format(string)


def not_after(string):
    return r"(?!{})".format(string)
