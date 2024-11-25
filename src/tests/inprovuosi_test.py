import unittest
from util import validate_year
from datetime import datetime


class test_inproyear(unittest.TestCase):
    def setUp(self):
        pass

    def test_positiivinen(self):
        self.assertTrue(validate_year(2019))

    def test_nolla(self):
        with self.assertRaises(ValueError, msg="Vuoden on oltava positiivinen"):
            validate_year(0)

    def test_negatiivinen(self):
        with self.assertRaises(ValueError, msg="Vuoden on oltava positiivinen"):
            validate_year(-200)

    def test_one(self):
        self.assertTrue(validate_year(1))

    def test_future(self):
        current_year = datetime.now().year

        self.assertTrue(validate_year(current_year))
        with self.assertRaises(ValueError, msg="Vuosi ei voi olla tulevaisuudessa"):
            validate_year(current_year + 1)
