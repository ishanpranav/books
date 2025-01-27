# bits.py
# Copyright (c) 2025 Ishan Pranav
# Licensed under the MIT license.

class DecodeError(Exception):
    pass
    
class ChunkError(Exception):
    pass

class BitList:
    def __init__(self, value):
        try:
            self.value = int(value, 2)
        except ValueError:
            raise ValueError(
                "Format is invalid; does not consist of only 0 and 1")

    def __eq__(self, other):
        return self.value == other.value
    
    def __str__(self):
        return format(self.value, 'b')
    
    def arithmetic_shift_left(self):
        self.value <<= 1
        
    def arithmetic_shift_right(self):
        self.value >>= 1
        
    @staticmethod
    def from_ints(*args):
        return BitList(''.join([ str(arg) for arg in args ]))