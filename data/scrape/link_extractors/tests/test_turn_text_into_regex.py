import unittest

from ..texts_allowed import turn_text_into_regex_pattern


class TestTurnTextIntoRegex(unittest.TestCase):
    def test_turn_into_pattern(self):
        for text, target in [
            ("test", ".*test.*"),
            ("^test", r"^\s*test.*"),
            ("test $", r".*test \s*$"),
            ("^test$", r"^\s*test\s*$"),
        ]:
            self.assertEqual(turn_text_into_regex_pattern(text), target)
