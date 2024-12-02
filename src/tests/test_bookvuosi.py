import unittest
from util import validate_year
from datetime import datetime


class Test_bookyear(unittest.TestCase):
    def setUp(self):
        pass

    def test_pos(self):
        self.assertTrue(validate_year(2022))

    def test_zero(self):
        with self.assertRaises(ValueError, msg="Vuoden on oltava positiivinen"):
            validate_year(0)

    def test_neg(self):
        with self.assertRaises(ValueError, msg="Vuoden on oltava positiivinen"):
            validate_year(-99)

    def test_one(self):
        self.assertTrue(validate_year(1))

    def test_future(self):
        current_year = datetime.now().year

        self.assertTrue(validate_year(current_year))
        with self.assertRaises(ValueError, msg="Vuosi ei voi olla tulevaisuudessa"):
            validate_year(current_year + 1)

    def test_non_integer(self):
        with self.assertRaises(ValueError, msg="Vuoden tulee olla kokonaisluku"):
            validate_year("2023")

    def test_float(self):
        with self.assertRaises(ValueError, msg="Vuoden tulee olla kokonaisluku"):
            validate_year(2023.5)
