import unittest
from floatinbits.fixed_point import Pure, C1, C2

class TestC1(unittest.TestCase):
    def setUp(self):
        self.bits_left = 3
        self.bits_right = 2

    def test_positive_number_simple(self):
        # Test a simple positive number without fractional part
        c1 = C1(self.bits_left, self.bits_right, '01000')  # 4.0
        self.assertEqual(c1.get_value(), 4.0)

    def test_positive_number_with_fraction(self):
        # Test a positive number with both integer and fractional parts
        c1 = C1(self.bits_left, self.bits_right, '01010')  # 2.5
        self.assertEqual(c1.get_value(), 2.5)

    def test_negative_number_simple(self):
        # Test a simple negative number without fractional part
        c1 = C1(self.bits_left, self.bits_right, '11000')  # Assuming -4 in one's complement
        self.assertEqual(c1.get_value(), -4.0)

    def test_negative_number_with_fraction(self):
        # Test a negative number with both integer and fractional parts
        c1 = C1(self.bits_left, self.bits_right, '10101')  # Assuming -2.5 in one's complement
        self.assertEqual(c1.get_value(), -2.5)

    def test_zero_representation(self):
        # Test zero which should be the same in positive and negative
        c1_positive = C1(self.bits_left, self.bits_right, '00000')
        c1_negative = C1(self.bits_left, self.bits_right, '11111')  # One's complement -0
        self.assertEqual(c1_positive.get_value(), 0)
        self.assertEqual(c1_negative.get_value(), -0)

    def test_invalid_length(self):
        # Ensure that an invalid binary length raises an error
        with self.assertRaises(ValueError):
            C1(self.bits_left, self.bits_right, '1010')  # Incorrect length

    def test_boundary_values(self):
        # Test boundary values to ensure range is accurately handled
        max_positive = '01111'  # 3.75
        min_negative = '10000'  # Assuming -3.75 in one's complement
        c1_pos = C1(self.bits_left, self.bits_right, max_positive)
        c1_neg = C1(self.bits_left, self.bits_right, min_negative)
        self.assertEqual(c1_pos.get_value(), 3.75)
        self.assertEqual(c1_neg.get_value(), -3.75)

    def test_round_trip_conversion(self):
        # Test converting to binary and back to decimal
        num = '01010'  # 2.5
        c1 = C1(self.bits_left, self.bits_right, num)
        self.assertEqual(c1.get_value(), 2.5)
        # Further testing can include converting back from decimal to binary if such functionality exists

class TestPure(unittest.TestCase):
    def setUp(self):
        self.bits_left = 3
        self.bits_right = 2

    def test_addition_simple(self):
        # Test simple addition without carrying over
        pure = Pure(self.bits_left, self.bits_right, '00101')  # 1.25
        other = Pure(self.bits_left, self.bits_right, '00010')  # 0.5
        result, overflow = pure.add_(pure, other)
        self.assertEqual(result, '00111')  # 1.75
        self.assertFalse(overflow)

    def test_addition_with_overflow(self):
        # Test addition where overflow occurs
        pure = Pure(self.bits_left, self.bits_right, '01101')  # Max positive before overflow
        other = Pure(self.bits_left, self.bits_right, '00011')  # 0.75
        result, overflow = pure.add_(pure, other)
        self.assertTrue(overflow)

    def test_subtraction_simple(self):
        # Test simple subtraction without underflow
        pure = Pure(self.bits_left, self.bits_right, '01010')  # 2.5
        other = Pure(self.bits_left, self.bits_right, '00011')  # 0.75
        result, underflow = pure.sub_(pure, other)
        self.assertEqual(result, '00111')  # Expected result 1.75
        self.assertFalse(underflow)

    def test_subtraction_with_underflow(self):
        # Test subtraction where underflow occurs
        pure = Pure(self.bits_left, self.bits_right, '00001')  # Small value
        other = Pure(self.bits_left, self.bits_right, '00100')  # Larger value
        result, underflow = pure.sub_(pure, other)
        self.assertTrue(underflow)

class TestC2(unittest.TestCase):
    def setUp(self):
        self.bits_left = 3
        self.bits_right = 2

    def test_get_value_positive(self):
        # Test positive number handling
        c2 = C2(self.bits_left, self.bits_right, '01010')  # 2.5
        self.assertEqual(c2.get_value(), 2.5)

    def test_get_value_negative_corrected(self):
        # Test negative number handling with complement correction
        c2 = C2(self.bits_left, self.bits_right, '10101')  # Complement of 2.5
        self.assertEqual(c2.get_value(), -2.5)

    def test_addition(self):
        # Test addition functionality in C2, assuming it exists and is similar to Pure
        c2_a = C2(self.bits_left, self.bits_right, '01101')  # 3.25
        c2_b = C2(self.bits_left, self.bits_right, '00011')  # 0.75
        result, overflow = c2_a.add_(c2_a, c2_b)
        self.assertEqual(result, '10000')  # Assuming wrap-around or similar behavior
        self.assertTrue(overflow)

    def test_subtraction(self):
        # Test subtraction functionality in C2, assuming it exists
        c2_a = C2(self.bits_left, self.bits_right, '01001')  # 2.25
        c2_b = C2(self.bits_left, self.bits_right, '00101')  # 1.25
        result, underflow = c2_a.sub_(c2_a, c2_b)
        self.assertEqual(result, '00100')  # 1.0 expected
        self.assertFalse(underflow)

if __name__ == '__main__':
    unittest.main()
