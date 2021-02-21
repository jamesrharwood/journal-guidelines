import unittest

from ..targets import TARGETS


class TestRegularExpressions(unittest.TestCase):
    pass


def match_test_factory(rex, test_data):
    if type(test_data) is str:
        a = b = test_data
    else:
        a, b = test_data[0], test_data[1]

    def test(self):
        match = rex.search(a)
        self.assertTrue(
            match, "{} not a match for regex: {}".format(a, rex.pattern[:30])
        )
        if type(b) == int:
            self.assertEqual(len(rex.findall(a)), b)
        else:
            self.assertEqual(match.group(), b)

    return test


def non_match_test_factory(rex, test_data):
    def test(self):
        self.assertFalse(
            rex.search(test_data),
            "{} should not be a match for regex: {}".format(
                test_data, rex.pattern[:20]
            ),
        )

    return test


for target in TARGETS:
    for pattern in target.patterns:
        for idx, m in enumerate(pattern.matches):
            test = match_test_factory(pattern, m)
            test_name = "test_match_{0}_{1}".format(pattern.name, idx)
            setattr(TestRegularExpressions, test_name, test)
        for idx, nm in enumerate(pattern.non_matches):
            test = non_match_test_factory(pattern, nm)
            test_name = "test_non_match_{0}_{1}".format(pattern.name, idx)
            setattr(TestRegularExpressions, test_name, test)


if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit as inst:
        if inst.args[0] is True:  # raised by sys.exit(True) when tests failed
            raise
