from floatingbits.core import NumericFormat, bin_to_hex

class FloatingPointFormat(NumericFormat):
    def __init__(self, exponent_bits, mantisa_bits):
        self.exponent_bits = exponent_bits
        self.mantissa_bits = mantisa_bits
        self.bit_length = exponent_bits + mantisa_bits + 1
        
        

class IEEE754(FloatingPointFormat):
    def __init__(self, bits_e, bits_m, num_rep, bit_implicito=1):
        self.bits_e = bits_e
        self.bits_m = bits_m
        self.excess = 2**(self.bits_e-1)-1
        if len(num_rep) != (1 + self.bits_e + self.bits_m):
            raise ValueError("La representación del número debe coincidir con la suma de bits_left y bits_right.")
        self.bin_rep = num_rep
        self.bit_implicito = bit_implicito
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
    
    def get_value(self):
        s = 1 if self.bin_rep[0] == '0' else -1
        exp, mant = self.split_binary()
        exp_v = int(exp,2) - self.excess 
        man_v = 1 if self.bit_implicito == 1 else 0
        if self.bit_implicito == 1:
            man_v = 1  + sum([mant[idx]* (2**-(idx+1)) for idx in range(len(mant))])
        else:
            man_v = .5 + sum([mant[idx]* (2**-(idx+2)) for idx in range(len(mant))])
        return s * (2**exp_v) * man_v