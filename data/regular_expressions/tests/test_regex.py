import unittest

from data.regular_expressions import RegularExpressions


class RegularExpressionsWithTestData(RegularExpressions):
    _matches = {}
    _non_matches = {}

    def _register_module(self, module):
        super()._register_module(module)
        self._matches.update({module.name: getattr(module, "matches")})
        self._non_matches.update({module.name: getattr(module, "non_matches")})


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


rx = RegularExpressionsWithTestData()

for pattern_name in rx:
    pattern = getattr(rx, pattern_name)
    matches = rx._matches[pattern_name]
    for idx, m in enumerate(matches):
        test = match_test_factory(pattern, m)
        test_name = "test_match_{0}_{1}".format(pattern_name, idx)
        setattr(TestRegularExpressions, test_name, test)
    non_matches = rx._non_matches[pattern_name]
    for idx, nm in enumerate(non_matches):
        test = non_match_test_factory(pattern, nm)
        test_name = "test_non_match_{0}_{1}".format(pattern_name, idx)
        setattr(TestRegularExpressions, test_name, test)


if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit as inst:
        if inst.args[0] is True:  # raised by sys.exit(True) when tests failed
            raise
