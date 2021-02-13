import unittest

from data.fields import FIELDS


class TestFields(unittest.TestCase):
    def test_fields_are_regitered(self):
        self.assertTrue(FIELDS._fields.keys())

    def test_iter(self):
        self.assertEqual(
            sum(len(collection) for collection in FIELDS._fields.values()),
            len(list(FIELDS)),
        )
