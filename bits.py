# bits.py
# Copyright (c) 2025 Ishan Pranav
# Licensed under the MIT license.

# References:
#  - https://docs.python.org/3/library/stdtypes.html#str.rjust

# CONSTRAINT: May not use `bytes` or `bytes.decode()`.

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
        return self.value == other.value and self.length == other.length
    
    def __str__(self):
        return format(self.value, 'b')
    
    def arithmetic_shift_left(self):
        self.value <<= 1
        
    def arithmetic_shift_right(self):
        value = self.value
        length = 0
        
        while value:
            value >>= 1
            length += 1
        
        if length == self.length:
            leftmost = 1 << (length - 1)
        else:
            leftmost = 0
                
        self.value = leftmost | (self.value >> 1)
    
    def bitwise_and(self, other):
        result = BitList('0')
        result.value = self.value & other.value
        result.length = self.length
            
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
    
    def decode(self, encoding = 'utf-8'):
        value = self.value
        result = ""
        
        match encoding:
            case 'us-ascii':
                while value:
                    result = chr(value & 0x7f) + result
                    value >>= 7
            
            case 'utf-8':
                trailings = { 0xf: 3, 0xe: 2, 0xc: 1 }
                stack = []
                
                while value:
                    stack.append(value & 0xff)
                    value >>= 8
                
                while len(stack):
                    leading = stack.pop() & 0xff
                    prefix = leading >> 4
                    
                    if prefix >> 3 == 0:
                        result += chr(leading)
                        continue
                    
                    if prefix not in trailings:
                        raise DecodeError("invalid leading byte")
                    
                    codepoint = leading & ((1 << (7 - trailings[prefix])) - 1)
                    
                    for i in range(trailings[prefix]):
                        if not len(stack):
                            raise DecodeError("invalid continuation byte")
                        
                        trailing = stack.pop() & 0xff
                        
                        if (trailing >> 6) & 0x3 != 0x2:
                            raise DecodeError("invalid continuation byte")
                        
                        codepoint = (codepoint << 6) | trailing & 0x3f
                        
                    result += chr(codepoint)
            
            case _: raise ValueError("encoding not supported")
            
        return result
        
    @staticmethod
    def from_ints(*args):
        return BitList("".join([ str(arg) for arg in args ]))
