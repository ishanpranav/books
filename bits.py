# bits.py
# Copyright (c) 2025 Ishan Pranav
# Licensed under the MIT license.

# References:
#  - https://docs.python.org/3/library/stdtypes.html#str.rjust

class DecodeError(Exception):
    pass
    
class ChunkError(Exception):
    pass

class BitList:
    def __init__(self, value):
        try:
            integral = int(value, 2)
        except ValueError:
            raise ValueError(
                "Format is invalid; does not consist of only 0 and 1")
            
        self.value = integral
        self.length = len(value)

    def __eq__(self, other):
        return self.value == other.value
    
    def __str__(self):
        return format(self.value, 'b')
    
    def arithmetic_shift_left(self):
        self.value <<= 1
        
    def arithmetic_shift_right(self):
        self.value >>= 1
    
    def bitwise_and(self, other):
        result = BitList('0')
        result.value = self.value & other.value
            
        return result
    
    def chunk(self, length):
        bits = str(self).rjust(self.length, '0')
        
        if len(bits) % length != 0:
            raise ChunkError(
                "the length of this instance is not divisible by 'length'")
        
        current = []
        results = []
        
        for bit in bits:
            current.append(int(bit))
            
            if len(current) == length:
                results.append(current)
                
                current = []
                
        return results
            
    @staticmethod
    def from_ints(*args):
        return BitList(''.join([ str(arg) for arg in args ]))
