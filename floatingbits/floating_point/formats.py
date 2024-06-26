import math
from typing import Union
from .base import FloatingPointFormat
from floatingbits.core import Mantissa, Exponent

class IEEE754(FloatingPointFormat):
    def __init__(self, value: Union[str, int, float], exponent_bits: int, mantissa_bits: int, excess_1: bool = True, implicit_bit: bool = True):
        super().__init__(exponent_bits, mantissa_bits)
        self.excess_1 = excess_1
        self.implicit_bit = implicit_bit
        self._initialize_value(value)

    def _initialize_value(self, value: Union[str, int, float]):
        if isinstance(value, str):
            self.from_binary(value)
        elif isinstance(value, (int, float)):
            self.from_decimal(value)
        else:
            raise ValueError("Input must be a binary string or a decimal number")

    def from_binary(self, binary: str):
        if len(binary) != self.bit_length:
            raise ValueError(f"Binary string must be {self.bit_length} bits long")
        self.sign     = -1 if binary[0] == '1' else 1
        self.exponent = Exponent(binary[1:1+self.exponent_bits], self.excess_1)
        self.mantissa = Mantissa(binary[1+self.exponent_bits:], self.implicit_bit)
        self.binary   = binary

    def from_decimal(self, decimal: float):
        self.sign = '1' if decimal < 0 else '0'
        decimal   = abs(decimal)
        
        if decimal == 0:
            exponent_value = 0
            mantissa_value = 0
        else:
            mantissa, exponent = math.frexp(decimal)
            exponent_value = exponent - 1 if self.excess_1 else exponent
            mantissa_value = int((mantissa * 2 - 1) * (1 << self.mantissa_bits))  # Ajusta la mantisa para llenar los bits

        sign_bit      = '1' if self.sign == -1 else '0'
        exponent_bits = format(exponent_value + (1 << (self.exponent_bits - 1)) - (1 if self.excess_1 else 0), f'0{self.exponent_bits}b')
        mantissa_bits = format(mantissa_value, f'0{self.mantissa_bits}b')
        
        self.binary   = sign_bit + exponent_bits + mantissa_bits
        self.exponent = Exponent(exponent_bits, self.excess_1)
        self.mantissa = Mantissa(mantissa_bits, self.implicit_bit)


    def get_value(self) -> float:
        return self.sign * float(self.mantissa) * (2 ** int(self.exponent))

    def add_(self, other: 'IEEE754') -> 'IEEE754':
        # Implementación básica de suma, puede mejorarse para mayor precisión
        result = self.get_value() + other.get_value()
        return IEEE754(result, self.exponent_bits, self.mantissa_bits, self.excess_1, self.implicit_bit)

    def sub_(self, other: 'IEEE754') -> 'IEEE754':
        # Implementación básica de resta, puede mejorarse para mayor precisión
        result = self.get_value() - other.get_value()
        return IEEE754(result, self.exponent_bits, self.mantissa_bits, self.excess_1, self.implicit_bit)

    def __repr__(self):
        return f"IEEE754(value={self.get_value():.6f}, binary='{self.binary}')"

# Ejemplo de uso
ieee_binary = IEEE754("01000000010010010000111111011011", 8, 23)
print(ieee_binary)  # Desde representación binaria
print(f"Exponent: {ieee_binary.exponent}")
print(f"Mantissa: {ieee_binary.mantissa}")

ieee_decimal = IEEE754(3.14159, 6, 5)
print(ieee_decimal)  # Desde valor decimal
print(f"Exponent: {ieee_decimal.exponent}")
print(f"Mantissa: {ieee_decimal.mantissa}")

result_add = ieee_binary.add_(ieee_decimal)
print(f"Addition result: {result_add}")

result_sub = ieee_binary.sub_(ieee_decimal)
print(f"Subtraction result: {result_sub}")