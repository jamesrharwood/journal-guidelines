import re
import unittest

from ..rx import RX


class TestRx(unittest.TestCase):
    def test_getattr(self):
        rx = RX(
            "test",
            r"\btest\b",
            matches=["test"],
            non_matches=["nope"],
            flags=re.I | re.M,
        )
        self.assertEqual(rx.flags, re.I | re.M)
        self.assertTrue(rx.search("test"))
