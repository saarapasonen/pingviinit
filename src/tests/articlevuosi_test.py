import unittest
from util import validate_year, UserInputError

#article vuosiluku oikeassa muodossa


class Testyear(unittest.TestCase):
    def setUp(self):
        pass

    def test_positive_year(self):
        self.assertTrue(validate_year(2023))

    def test_zero_year(self):
        with self.assertRaises(ValueError, msg="Vuoden on oltava positiivinen"):
            validate_year(0)

    def test_negative_year(self):
        with self.assertRaises(ValueError, msg="Vuoden on oltava positiivinen"):
            validate_year(-100)
