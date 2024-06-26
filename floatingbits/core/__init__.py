from .utils import *
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