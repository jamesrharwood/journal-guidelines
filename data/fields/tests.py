from data.preprocess.load.strategies import text_from_tag
from data.preprocess.load.fields import LoadedFieldBase
import unittest
from data import preprocess

from data.fields import FIELDS
from data.preprocess.load import fields as loaded


class TestFields(unittest.TestCase):
    def test_fields_are_regitered(self):
        self.assertTrue(FIELDS._fields)

    def test_iter_by_type(self):
        text_field_count = len(list(FIELDS.iter_by_class(loaded.TextField)))
        list_field_count = len(list(FIELDS.iter_by_class(loaded.ListField)))
        loaded_field_count = len(list(FIELDS.iter_by_class(loaded.LoadedFieldBase)))
        self.assertTrue(text_field_count)
        self.assertTrue(list_field_count)
        self.assertEqual(text_field_count + list_field_count, loaded_field_count)
