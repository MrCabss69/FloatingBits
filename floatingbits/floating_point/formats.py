from floatingbits.core import bin_to_hex
from floatingbits.floating_point.base import FloatingPointFormat

class IEEE754(FloatingPointFormat):
    def __init__(self, bits_e, bits_m, num_rep, bit_implicito=True):
        self.bits_e = bits_e
        self.bits_m = bits_m
        self.excess = 2**(self.bits_e-1)-1
        if len(num_rep) != (1 + self.bits_e + self.bits_m):
            raise ValueError("La representación del número debe coincidir con la suma de bits para el signo, exponente y mantisa.")
        self.bin_rep = num_rep
        self.bit_implicito = bit_implicito
        self.decimal_value = self.get_value()
        self.hex_rep = bin_to_hex(self.bin_rep)

    def get_value(self):
        s = -1 if self.bin_rep[0] == '1' else 1
        exp = int(self.bin_rep[1:1+self.bits_e], 2) - self.excess
        mant_bin = self.bin_rep[1+self.bits_e:]
        if self.bit_implicito:
            
            man_v = 1  + sum(int(mant_bin[idx]) * (2**-(idx+1)) for idx in range(len(mant_bin)))
        else:
            man_v = .5 + sum(int(mant_bin[idx]) * (2**-(idx+2)) for idx in range(len(mant_bin)))
        return s * (2**exp) * man_v

