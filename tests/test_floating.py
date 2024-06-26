import unittest
import math
from floatingbits.floating_point import IEEE754


class TestIEEE754(unittest.TestCase):

    def test_initialization_with_binary(self):
        ieee = IEEE754('01000000010010010000111111011011', 8, 23)
        self.assertAlmostEqual(ieee.get_value(), 3.14, places=2)

    def test_initialization_with_decimal(self):
        ieee = IEEE754(3.14, 8, 23)
        expected_binary = '01000000010010010000111111011011'  # Esto podría no ser exactamente 3.14 debido a la precisión
        self.assertEqual(ieee.binary, expected_binary)

    def test_invalid_input_type(self):
        with self.assertRaises(ValueError):
            IEEE754({}, 8, 23)

    def test_binary_length_error(self):
        with self.assertRaises(ValueError):
            IEEE754('1011', 8, 23)  # Longitud incorrecta

    def test_addition(self):
        ieee1 = IEEE754(1.5, 8, 23)
        ieee2 = IEEE754(2.5, 8, 23)
        result = ieee1.add_(ieee2)
        self.assertAlmostEqual(result.get_value(), 4.0, places=5)

    def test_subtraction(self):
        ieee1 = IEEE754(3.5, 8, 23)
        ieee2 = IEEE754(2.0, 8, 23)
        result = ieee1.sub_(ieee2)
        self.assertAlmostEqual(result.get_value(), 1.5, places=5)

    def test_representation(self):
        ieee = IEEE754(3.14, 8, 23)
        repr_string = repr(ieee)
        self.assertIn("IEEE754(value=3.140000", repr_string)

if __name__ == '__main__':
    unittest.main()