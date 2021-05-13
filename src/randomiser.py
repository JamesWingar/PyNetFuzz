import random

class Randomiser():

    def __init__(self, seed=None):
        self.seed = seed
        random.seed(seed)
        
    
    def ip(self, ip_str):
        return '.'.join([str(self.bit_8()) if byte == '*' else byte for byte in ip_str.split('.')])

    def mac(self):
        return '00:' + ':'.join([hex(self.bit_8()).lstrip('0x') for octet in range(5)])

    def port(self):
        return self.bit_16()

    def boolean(self):
        return random.randint(0, 1) == 1

    def type(self, length):
        return random.randint(0, length - 1)

    def choose(self, choices):
        return choices[random.randint(0, len(choices) - 1)]

    def bit_32(self):
        return random.randint(0, 2147483647)

    def bit_16(self):
        return random.randint(0, 65535)

    def bit_13(self):
        return random.randint(0, 8191)

    def bit_8(self):
        return random.randint(0, 255)

    def bit_2(self):
        return random.randint(0, 3)
