from floatingbits.core import bin_to_hex, NumericFormat

class FixedPointFormat(NumericFormat):
    def __init__(self, bits_left, bits_right, number_representation):
        self.bits_left = bits_left
        self.bits_right = bits_right
        if len(number_representation) != (self.bits_left + self.bits_right):
            raise ValueError("La representación del número debe coincidir con la suma de bits_left y bits_right.")
        self.bin_rep = number_representation
        self.decimal_value = self.get_value()
        self.hex_rep = bin_to_hex(self.bin_rep)

    def split_binary(self):
        """Divide el binario en parte entera y fraccional según los bits especificados."""
        return self.bin_rep[1:self.bits_left], self.bin_rep[self.bits_left:]

    def binary_to_decimal(self, int_part, float_part):
        """Convierte las partes entera y fraccional de un binario a su equivalente decimal."""
        int_value = int(int_part, 2)
        float_value = sum((int(bit) * 2**-i) for i, bit in enumerate(float_part, 1))
        return int_value, float_value