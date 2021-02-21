import unittest

from ..targets import TARGETS, GUIDELINES


class TestGuidelineTargets(unittest.TestCase):
    def test_guidelines_and_targets_load(self):
        guidelines = [gl for gl in GUIDELINES]
        self.assertTrue(guidelines)
        self.assertTrue(TARGETS)
        self.assertTrue(len(TARGETS) > len(guidelines))
        for gl in guidelines:
            self.assertTrue(gl in TARGETS)
