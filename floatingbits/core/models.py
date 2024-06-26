from abc import ABC, abstractmethod

class NumericFormat(ABC):
    """Abstract base class."""
    @abstractmethod
    def get_value(self):
        pass
    
    @abstractmethod
    def add_(self,a,b):
        pass
    
    @abstractmethod
    def sub_(self,a,b):
        pass
    
    
    
class Exponent:
    def __init__(self, binary_representation: str, excess_1: bool = True):
        self.binary_rep = binary_representation
        self.excess_1 = excess_1
        self.excess = (1 << (len(binary_representation) - 1)) - (1 if excess_1 else 0)
        self.value = int(binary_representation, 2) - self.excess

    def __int__(self):
        return self.value

    def __repr__(self):
        return f"Exponent(value={self.value}, binary='{self.binary_rep}')"



class Mantissa:
    def __init__(self, binary_representation: str, implied_bit_left: bool = True):
        self.binary_rep = binary_representation
        self.implied_bit = implied_bit_left
        if self.implied_bit:
            self.value = 1
            self.value += sum([2**-(idx+1) if binary_representation[idx] == '1' else 0 for idx in range(len(binary_representation)) ])
        else:
            self.value = 0.5
            self.value += sum([2**-(idx+2) if binary_representation[idx] == '1' else 0 for idx in range(len(binary_representation)) ])

    def __float__(self):
        return self.value

    def __repr__(self):
        return f"Mantissa(value={self.value:.6f}, binary='{self.binary_rep}')"