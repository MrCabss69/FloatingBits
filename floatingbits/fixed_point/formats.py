from floatingbits.core import bin_plus_one
from floatingbits.fixed_point.base import FixedPointFormat

class Pure(FixedPointFormat):
    """Implementación específica que maneja operaciones binarias directamente."""
    
    def __init__(self, bits_left, bits_right, number_representation):
        super().__init__(bits_left, bits_right, number_representation)
        self.resolution = 2**-bits_right
        self.range = [ 0 , 2**bits_left -  self.resolution ]

    def get_value(self):
        """Calcula y devuelve el valor decimal a partir de la representación binaria."""
        int_part, float_part = self.split_binary()
        int_value, float_value = self.binary_to_decimal(int_part, float_part)
        return int_value + float_value

    def add_(self, a, b):
        """Realiza una suma binaria entre dos números en el formato, manejando acarreos."""
        result = []
        carry = 0
        for i in range(self.bits_left + self.bits_right - 1, -1, -1):
            bit_a = int(a.bin_rep[i])
            bit_b = int(b.bin_rep[i])
            total = bit_a + bit_b + carry
            if total >= 2:
                result.append('1')
                carry = 1
            else:
                result.append(str(total))
                carry = 0
        overflow = carry
        result.reverse()
        return ''.join(result), overflow

    def sub_(self, a, b):
        """Realiza una resta binaria entre dos números en el formato, manejando préstamos."""
        result = []
        borrow = 0
        for i in range(self.bits_left + self.bits_right - 1, -1, -1):
            bit_a = int(a.bin_rep[i])
            bit_b = int(b.bin_rep[i])
            total = bit_a - bit_b - borrow
            if total < 0:
                result.append('1')
                borrow = 1
            else:
                result.append(str(total))
                borrow = 0
        underflow = borrow
        result.reverse()
        return ''.join(result), underflow


class C1(FixedPointFormat):
    def __init__(self, bits_left, bits_right, number_representation):
        super().__init__(bits_left, bits_right, number_representation)
        self.resolution = 2**-bits_right
        self.range = [[-2**(bits_left-1), 2**(bits_left-1) - 1]]
        
        
    def get_value(self):
        int_part, float_part = self.split_binary()
        if self.bin_rep[0] == '1':
            int_part = ''.join('1' if bit == '0' else '0' for bit in int_part)
            float_part = ''.join('1' if bit == '0' else '0' for bit in float_part)
        int_value, float_value = self.binary_to_decimal(int_part, float_part)
        return - (int_value + float_value) if self.bin_rep[0] == '1' else (int_value + float_value)
    
    def add_(self,a,b):
        result = []
        carry = 0
        for i in range(self.bits_left + self.bits_right - 1, -1, -1):
            bit_a = int(a.bin_rep[i])
            bit_b = int(b.bin_rep[i])
            total = bit_a + (bit_b + carry)
            if total >= 2:
                result.append('1')
                carry = 1
            else:
                result.append(str(total))
                carry = 0
        overflow = carry
        result.reverse()
        result = ''.join(result)
        if overflow > 0:
            result = bin_plus_one(result)
        return result, overflow
    
    
    def sub_(self, a, b):
        """Realiza una resta binaria entre dos números en el formato, manejando préstamos."""
        result = []
        borrow = 0
        for i in range(self.bits_left + self.bits_right - 1, -1, -1):
            bit_a = int(a.bin_rep[i])
            bit_b = int(b.bin_rep[i])
            total = bit_a - bit_b - borrow
            if total < 0:
                result.append('1')
                borrow = 1 
            else:
                result.append(str(total))
                borrow = 0
        underflow = borrow
        result.reverse() 
        return ''.join(result), underflow

        
        

class C2(FixedPointFormat):
    """Implementación específica de C2"""
    def get_value(self):
        sign_bit = self.bin_rep[0]
        int_part, float_part = self.split_binary()
        
        if sign_bit == '1':
            inverted_bin = ''.join('1' if bit == '0' else '0' for bit in int_part + float_part)
            corrected_bin = bin_plus_one(inverted_bin)
            int_part = corrected_bin[:self.bits_left - 1]
            float_part = corrected_bin[self.bits_left - 1:]
        
        int_value, float_value = self.binary_to_decimal(int_part, float_part)
        return - (int_value + float_value) if sign_bit == '1' else (int_value + float_value)

