from floatingbits.abstract import NumericFormat

class FloatingPointFormat(NumericFormat):
    def __init__(self, exponent_bits, mantisa_bits):
        self.exponent_bits = exponent_bits
        self.mantisa_bits = mantisa_bits
        self.bit_length = exponent_bits + mantisa_bits + 1