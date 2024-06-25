from floatingbits.core import bin_to_hex
from floatingbits.floating_point.base import FloatingPointFormat



class Exponent:
    def __init__(self, binary_representation, excess_1=True):
        self.binary_rep = binary_representation
        self.excess_1 = excess_1
        self.excess = 2 ** (len(binary_representation) - 1)
        if excess_1:
            self.excess -= 1
        self.value = int(binary_representation, 2) - self.excess

class Mantissa:
    def __init__(self, binary_representation, implied_bit=True):
        self.binary_rep = binary_representation
        self.implied_bit = implied_bit
        self.value = 1.0 if implied_bit else 0.5
        self.value += sum(int(bit) * (2 ** -(idx + 1)) for idx, bit in enumerate(binary_representation))
        

class IEEE754:
    def __init__(self, binary_representation, exponent_bits, excess=True, implied_bit=True):
        self.binary_rep = binary_representation
        self.exponent_bits = exponent_bits
        self.sign = -1 if binary_representation[0] == '1' else 1
        self.exponent = Exponent(binary_representation[1:1 + exponent_bits], excess)
        self.mantissa = Mantissa(binary_representation[1 + exponent_bits:], implied_bit)

    def get_value(self):
        return self.sign * (2 ** self.exponent.value) * self.mantissa.value
    
    
    def from_decimal(self,decimal_value):
        # dv = s * (2 ** self.exponent.value) * self.mantissa.value
        

    def add(self, other):
        # Adjust exponents to match
        exp_diff = self.exponent.value - other.exponent.value
        self_mantissa_shifted = self.shift_mantissa(self.mantissa.binary_rep, -exp_diff) if exp_diff < 0 else self.mantissa.binary_rep
        other_mantissa_shifted = self.shift_mantissa(other.mantissa.binary_rep, exp_diff) if exp_diff > 0 else other.mantissa.binary_rep

        # Binary addition considering sign
        if self.sign == other.sign:
            result_mantissa = self.binary_add(self_mantissa_shifted, other_mantissa_shifted)
        else:
            result_mantissa = self.binary_subtract(self_mantissa_shifted, other_mantissa_shifted)
            # Adjust sign if needed
            if result_mantissa.startswith('-'):
                result_mantissa = result_mantissa[1:]
                self.sign *= -1

        # Normalize and round the result
        result_mantissa, result_exponent = self.normalize(result_mantissa, self.exponent.value if exp_diff >= 0 else other.exponent.value)
        result_binary = self.convert_to_binary(self.sign, result_exponent, result_mantissa)
        return IEEE754(result_binary, self.exponent_bits, self.exponent.excess_1, self.mantissa.implied_bit)

    def shift_mantissa(self, mantissa, places):
        # Shift mantissa right by 'places' places in binary
        return '0' * abs(places) + mantissa if places < 0 else mantissa + '0' * places

    def binary_add(self, mantissa1, mantissa2):
        # Binary addition of two mantissas
        max_len = max(len(mantissa1), len(mantissa2))
        mantissa1 = mantissa1.zfill(max_len)
        mantissa2 = mantissa2.zfill(max_len)
        result = ''
        carry = 0
        for i in range(max_len - 1, -1, -1):
            total = int(mantissa1[i]) + int(mantissa2[i]) + carry
            result = str(total % 2) + result
            carry = total // 2
        if carry:
            result = '1' + result
        return result

    def binary_subtract(self, mantissa1, mantissa2):
        # Perform binary subtraction of two mantissas (mantissa1 - mantissa2)
        max_len = max(len(mantissa1), len(mantissa2))
        mantissa1 = mantissa1.zfill(max_len)
        mantissa2 = mantissa2.zfill(max_len)
        result = ''
        borrow = 0
        for i in range(max_len - 1, -1, -1):
            diff = int(mantissa1[i]) - int(mantissa2[i]) - borrow
            if diff < 0:
                diff += 2
                borrow = 1
            else:
                borrow = 0
            result = str(diff) + result
        if borrow:
            # This means mantissa1 < mantissa2, result will be negative
            result = '-' + self.binary_subtract(mantissa2, mantissa1)
        return result.strip('0') or '0'  # Remove leading zeros

    def normalize(self, mantissa, exponent):
        # Normalize the binary mantissa
        # Find the first '1' in mantissa to normalize
        first_one_index = mantissa.find('1')
        if first_one_index == -1:
            return '0', 0  # Mantissa is zero
        # Shift the mantissa to the right to normalize
        shift_count = first_one_index
        mantissa = mantissa[first_one_index:]
        exponent -= shift_count
        return mantissa, exponent

    def convert_to_binary(self, sign, exponent, mantissa):
        # Construct the full binary representation from sign, exponent, and mantissa
        binary_sign = '1' if sign < 0 else '0'
        binary_exponent = format(exponent + self.exponent.excess, '0{}b'.format(len(self.exponent.binary_rep)))
        binary_mantissa = mantissa.lstrip('1')[1:]  # Remove the leading '1' for the implicit bit
        return f"{binary_sign}{binary_exponent}{binary_mantissa}"
