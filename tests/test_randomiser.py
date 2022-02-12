"""
Unit tests for Randomiser class
"""
import unittest
# Package imports
import pynetfuzz.exceptions as ex
# Module under test
from pynetfuzz.randomiser import Randomiser

# Testing the Randomiser Class
class TestRandomiser(unittest.TestCase):
    """ Testing Randomiser class and methods"""

    def test_valid_init(self):
        """ Test valid initialising parameters"""
        # Correct random seed initialisation test
        self.assertEqual(Randomiser(1).seed, 1)
        self.assertEqual(type(Randomiser().seed), int)
        self.assertEqual(Randomiser(9234.7103).seed, 9234)
        self.assertEqual(Randomiser(1934580).seed, 1934580)

    def test_invalid_init(self):
        """ Test invalid initialising parameters"""
        # Incorrect argument datatype tests
        with self.assertRaises(ex.SeedInvalidValueError):
            Randomiser(-192200949580)
        with self.assertRaises(ex.SeedInvalidFormatError):
            Randomiser("hello")

    def test_valid_ip(self):
        """ Test valid ip randomise method"""
        # Random int (0-255) Sequence: 68 32 130 60 253 230 241 194
        seed = 1
        # Correct random IP generation
        self.assertEqual(Randomiser(seed).ipaddr("192.168.1.24"), "192.168.1.24")
        self.assertEqual(Randomiser(seed).ipaddr("192.168.1.*"), "192.168.1.68")
        self.assertEqual(Randomiser(seed).ipaddr("192.168.*.*"), "192.168.68.32")
        self.assertEqual(Randomiser(seed).ipaddr("192.*.*.*"), "192.68.32.130")
        self.assertEqual(Randomiser(seed).ipaddr("*.*.*.*"), "68.32.130.60")
        self.assertEqual(Randomiser(seed).ipaddr(), "68.32.130.60")
        self.assertEqual(Randomiser(seed).ipaddr(), Randomiser(seed).ipaddr("*.*.*.*"))

    def test_invalid_ipaddr(self):
        """ Test invalid ipaddr randomise method"""
        # Random int (0-255) Sequence: 68 32 130 60 253 230 241 194
        seed = 1
        # Incorrect argument datatype tests
        with self.assertRaises(ex.IpAddressInvalidTypeError):
            Randomiser(seed).ipaddr(1)
        with self.assertRaises(ex.IpAddressInvalidTypeError):
            Randomiser(seed).ipaddr(123.456)
        with self.assertRaises(ex.IpAddressInvalidTypeError):
            Randomiser(seed).ipaddr(False)
        # Incorrect String Form tests
        with self.assertRaises(ex.IpScopeAddressInvalidFormatError):
            Randomiser(seed).ipaddr("Marilyn Monroe")
        with self.assertRaises(ex.IpScopeAddressInvalidFormatError):
            Randomiser(seed).ipaddr("123-123.123.123")
        with self.assertRaises(ex.IpScopeAddressInvalidFormatError):
            Randomiser(seed).ipaddr("58.129.245")
        with self.assertRaises(ex.IpScopeAddressInvalidFormatError):
            Randomiser(seed).ipaddr("198.63.154.256")
        with self.assertRaises(ex.IpAddressTooLongValueError):
            Randomiser(seed).ipaddr("39wrnvkdsnv.4903wr.fosief.309")

    def test_mac(self):
        """ Test mac address randomise method"""
        seeds = {
            # Seed: 11 - Random int (0-255) Sequence (dec): 231 238 231 97 94
            # Seed: 11 - Random int (0-255) Sequence (hex): E7 EE E7 61 5E
            11: "00:E7:EE:E7:61:5E",
            # Seed: 21 - Random int (0-255) Sequence (dec): 84 214 214 144 245
            # Seed: 21 - Random int (0-255) Sequence (hex): 54 D6 D6 90 F5
            21: "00:54:D6:D6:90:F5",
            # Seed: 31 - Random int (0-255) Sequence (dec): 6 240 57 201 72
            # Seed: 31 - Random int (0-255) Sequence (hex): 6 F0 39 C9 48
            31: "00:6:F0:39:C9:48",
            # Seed: 41 - Random int (0-255) Sequence (dec): 195 170 118 85 197
            # Seed: 41 - Random int (0-255) Sequence (hex): C3 AA 76 55 C5
            41: "00:C3:AA:76:55:C5",
            # Seed: 51 - Random int (0-255) Sequence (dec): 124 82 125 118 130
            # Seed: 51 - Random int (0-255) Sequence (hex): 7C 52 7D 76 82
            51: "00:7C:52:7D:76:82",
        }
        for seed, result in seeds.items():
            self.assertEqual(Randomiser(seed).mac(), result)

    def test_boolean(self):
        """ Test bool value randomise method"""
        # Seed: 61 - Random int (0-1) Sequence: 1 0 0 1 1
        seed, results = 61, [True, False, False, True, True]
        randomiser = Randomiser(seed)
        for result in results:
            self.assertEqual(randomiser.boolean(), result)

    def test_valid_index(self):
        """ Test valid index randomise method"""
        seed = 71 # Random int (0, length - 1)
        randomiser = Randomiser(seed)
        # Correct random index generation
        self.assertEqual(randomiser.index(100), 41)
        self.assertEqual(randomiser.index(1), 0)
        self.assertEqual(randomiser.index(1234), 542)
        self.assertEqual(randomiser.index(9999), 2536)
        self.assertEqual(randomiser.index(65535), 53880)

    def test_invalid_index(self):
        """ Test invalid index randomise method"""
        seed = 71 # Random int (0, length - 1)
        # Incorrect argument datatype tests
        with self.assertRaises(ex.IntegerInvalidFormatError):
            Randomiser(seed).index("Marilyn Monroe")
        # Incorrect argument value tests
        with self.assertRaises(ex.IntegerTooSmallError):
            Randomiser(seed).index(-10)

    def test_valid_choose(self):
        """ Test valid choose randomise method"""
        # Seed: 81 - Random int (0, length - 1) Sequence: 8 7 5 8 8
        seed_1 = 81
        # Seed: 91 - Random int (0, length - 1) Sequence: 1 9 2 10 10
        seed_2 = 91
        test_list = [
            1, 2, 3,
            "Spaghetti", "Meatballs", "Lasagne",
            1.234, 2.345, 3.456,
            False, True, False]
        # Correct random choice generation
        randomiser = Randomiser(seed_1)
        self.assertEqual(randomiser.choose(test_list), 3.456)
        self.assertEqual(randomiser.choose(test_list), 2.345)
        self.assertEqual(randomiser.choose(test_list), "Lasagne")
        self.assertEqual(randomiser.choose(test_list), 3.456)
        self.assertEqual(randomiser.choose(test_list), 3.456)
        randomiser = Randomiser(seed_2)
        self.assertEqual(randomiser.choose(test_list), 2)
        self.assertEqual(randomiser.choose(test_list), False)
        self.assertEqual(randomiser.choose(test_list), 3)
        self.assertEqual(randomiser.choose(test_list), True)
        self.assertEqual(randomiser.choose(test_list), True)

    def test_invalid_choose(self):
        """ Test invalid choose randomise method"""
        seed = 81 # Random int (0, length - 1)
        # Incorrect argument datatype tests
        with self.assertRaises(TypeError):
            Randomiser(seed).choose(123.456)
        with self.assertRaises(TypeError):
            Randomiser(seed).choose(False)
        with self.assertRaises(TypeError):
            Randomiser(seed).choose({"Hello": 1})
        # Incorrect argument value tests
        with self.assertRaises(ValueError):
            Randomiser(seed).choose([])

    def test_valid_rand(self):
        """ Test valid choose randomise method"""
        seed = 101  # Random int (min, max)

        # Correct random value generation
        randomiser = Randomiser(seed)
        self.assertEqual(randomiser.rand(0, 100), 74)
        self.assertEqual(randomiser.rand(200, 65535), 55716)
        self.assertEqual(randomiser.rand(-67, 76), -18)
        self.assertEqual(randomiser.rand(-1, 1), 1)
        self.assertEqual(randomiser.rand(-65535, -50051), -50397)

    def test_invalid_rand(self):
        """ Test invalid choose randomise method"""
        seed = 101  # Random int (min, max)
        # Incorrect argument datatype tests
        with self.assertRaises(TypeError):
            Randomiser(seed).rand("Marilyn Monroe", 1)
        with self.assertRaises(TypeError):
            Randomiser(seed).rand(2, 123.456)
        with self.assertRaises(TypeError):
            Randomiser(seed).rand({"Hello": 1}, 2)
        with self.assertRaises(TypeError):
            Randomiser(seed).rand((5, 6), 4)
        # Incorrect argument value tests
        with self.assertRaises(ValueError):
            Randomiser(seed).rand(0, -5)
        with self.assertRaises(ValueError):
            Randomiser(seed).rand(-5, -100)
        with self.assertRaises(ValueError):
            Randomiser(seed).rand(70, 68)

    def test_bit(self):
        """ Test bit randomise method"""
        seed = 111 # Random int (0, bit)
        # Correct random choice generation
        randomiser = Randomiser(seed)
        self.assertEqual(randomiser.bit_32(), 913810597)
        self.assertEqual(randomiser.bit_20(), 662646)
        self.assertEqual(randomiser.bit_16(), 64739)
        self.assertEqual(randomiser.bit_13(), 3181)
        self.assertEqual(randomiser.bit_8(), 203)
        self.assertEqual(randomiser.bit_3(), 6)
        self.assertEqual(randomiser.bit_2(), 1)
        self.assertEqual(randomiser.bit_32(), 831557934)
        self.assertEqual(randomiser.bit_20(), 884253)
        self.assertEqual(randomiser.bit_16(), 30107)
        self.assertEqual(randomiser.bit_13(), 3003)
        self.assertEqual(randomiser.bit_8(), 237)
        self.assertEqual(randomiser.bit_3(), 6)
        self.assertEqual(randomiser.bit_2(), 3)

if __name__ == "__main__":
    unittest.main()
