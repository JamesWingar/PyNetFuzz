import unittest
from src import const

# Module under test
from src.randomiser import Randomiser


# Testing the Randomiser Class
class TestRandomiser(unittest.TestCase):

    def test_init(self):
        # Correct random seed initialisation test
        self.assertEqual(Randomiser(1).seed, 1)
        self.assertEqual(type(Randomiser().seed), int)
        self.assertEqual(Randomiser(1934580).seed, 1934580)
        self.assertEqual(Randomiser(-192200949580).seed, -192200949580)

        # Incorrect argument datatype tests
        with self.assertRaises(TypeError) as exception:
            Randomiser(23.176)
        with self.assertRaises(TypeError) as exception:
            Randomiser(9234.7103)
        with self.assertRaises(TypeError) as exception:
            Randomiser(False)
        with self.assertRaises(TypeError) as exception:
            Randomiser("hello")
        with self.assertRaises(TypeError) as exception:
            Randomiser("1")
        with self.assertRaises(TypeError) as exception:
            Randomiser("/0-/23-/")


    def test_ip(self):
        # Random int (0-255) Sequence: 68 32 130 60 253 230 241 194
        seed = 1

        # Correct random IP generation
        self.assertEqual(Randomiser(seed).ip("192.168.1.24"), "192.168.1.24")
        self.assertEqual(Randomiser(seed).ip("192.168.1.*"), "192.168.1.68")
        self.assertEqual(Randomiser(seed).ip("192.168.*.*"), "192.168.68.32")
        self.assertEqual(Randomiser(seed).ip("192.*.*.*"), "192.68.32.130")
        self.assertEqual(Randomiser(seed).ip("*.*.*.*"), "68.32.130.60")
        self.assertEqual(Randomiser(seed).ip(), "68.32.130.60")
        self.assertEqual(Randomiser(seed).ip(), Randomiser(seed).ip("*.*.*.*"))

        # Incorrect argument datatype tests
        with self.assertRaises(TypeError) as exception:
            Randomiser(seed).ip(1)
        with self.assertRaises(TypeError) as exception:
            Randomiser(seed).ip(123.456)
        with self.assertRaises(TypeError) as exception:
            Randomiser(seed).ip(False)

        # Incorrect String Form tests
        with self.assertRaises(ValueError) as exception:
            Randomiser(seed).ip("Marilyn Monroe")
        with self.assertRaises(ValueError) as exception:
            Randomiser(seed).ip("39wrnvkdsnv.4903wr.fosief. 309")
        with self.assertRaises(ValueError) as exception:
            Randomiser(seed).ip("123-123.123.123")
        with self.assertRaises(ValueError) as exception:
            Randomiser(seed).ip("58.129.245")
        with self.assertRaises(ValueError) as exception:
            Randomiser(seed).ip("198.63.154.256")


    def test_mac(self):
        seeds = {
            # Random int (0-255) Sequence (dec): 231 238 231 97 94
            # Random int (0-255) Sequence (hex): E7 EE E7 61 5E
            11: "00:E7:EE:E7:61:5E",
            # Random int (0-255) Sequence (dec): 84 214 214 144 245
            # Random int (0-255) Sequence (hex): 54 D6 D6 90 F5
            21: "00:54:D6:D6:90:F5", 
            # Random int (0-255) Sequence (dec): 6 240 57 201 72
            # Random int (0-255) Sequence (hex): 6 F0 39 C9 48
            31: "00:6:F0:39:C9:48",
            # Random int (0-255) Sequence (dec): 195 170 118 85 197
            # Random int (0-255) Sequence (hex): C3 AA 76 55 C5
            41: "00:C3:AA:76:55:C5",
            # Random int (0-255) Sequence (dec): 124 82 125 118 130
            # Random int (0-255) Sequence (hex): 7C 52 7D 76 82
            51: "00:7C:52:7D:76:82",
        }
        for seed, result in seeds.items():
            self.assertEqual(Randomiser(seed).mac(), result)


    def test_boolean(self):
        # Random int (0-1) Sequence: 1 0 0 1 1
        seed, results = 61, [True, False, False, True, True]

        randomiser = Randomiser(seed)
        for result in results:
            self.assertEqual(randomiser.boolean(), result)


    def test_type(self):
        # Random int (0, length - 1)
        seed = 71
        randomiser = Randomiser(seed)
        
        # Correct random type generation
        self.assertEqual(randomiser.type(100), 41)
        self.assertEqual(randomiser.type(1), 0)
        self.assertEqual(randomiser.type(1234), 542)
        self.assertEqual(randomiser.type(9999), 2536)
        self.assertEqual(randomiser.type(65535), 53880)

        # Incorrect argument datatype tests
        with self.assertRaises(TypeError) as exception:
            Randomiser(seed).type("Marilyn Monroe")
        with self.assertRaises(TypeError) as exception:
            Randomiser(seed).type(123.456)
        with self.assertRaises(TypeError) as exception:
            Randomiser(seed).type(False)

        # Incorrect argument value tests
        with self.assertRaises(ValueError) as exception:
            Randomiser(seed).type(0)
        with self.assertRaises(ValueError) as exception:
            Randomiser(seed).type(-10)


    def test_choose(self):
        # Random int (0, length - 1) Sequence: 8 7 5 8 8
        seed_1 = 81
        # Random int (0, length - 1) Sequence: 1 9 2 10 10
        seed_2 = 91
        test_list = [
            1, 2, 3,
            "Spaghetti", "Meatballs", "Lasagne",
            1.234, 2.345, 3.456,
            False, True, False
        ]

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

        # Incorrect argument datatype tests
        with self.assertRaises(TypeError) as exception:
            Randomiser(seed_1).choose(123.456)
        with self.assertRaises(TypeError) as exception:
            Randomiser(seed_1).choose(False)
        with self.assertRaises(TypeError) as exception:
            Randomiser(seed_1).choose({"Hello": 1})

        # Incorrect argument value tests
        with self.assertRaises(ValueError) as exception:
            Randomiser(seed_1).choose([])

    
    def test_rand(self):
        # Random int (min, max)
        seed = 101

        # Correct random value generation
        randomiser = Randomiser(seed)
        self.assertEqual(randomiser.rand(0, 100), 74)
        self.assertEqual(randomiser.rand(200, 65535), 55716)
        self.assertEqual(randomiser.rand(-67, 76), -18)
        self.assertEqual(randomiser.rand(-1, 1), 1)
        self.assertEqual(randomiser.rand(-65535, -50051), -50397)

        # Incorrect argument datatype tests
        with self.assertRaises(TypeError) as exception:
            Randomiser(seed).rand("Marilyn Monroe", 1)
        with self.assertRaises(TypeError) as exception:
            Randomiser(seed).rand(2, 123.456)
        with self.assertRaises(TypeError) as exception:
            Randomiser(seed).rand(False, 3)
        with self.assertRaises(TypeError) as exception:
            Randomiser(seed).rand({"Hello": 1}, 2)
        with self.assertRaises(TypeError) as exception:
            Randomiser(seed).rand((5, 6), 4)

        # Incorrect argument value tests
        with self.assertRaises(ValueError) as exception:
            Randomiser(seed).rand(0, -5)
        with self.assertRaises(ValueError) as exception:
            Randomiser(seed).rand(-5, -100)
        with self.assertRaises(ValueError) as exception:
            Randomiser(seed).rand(70, 68)


    def test_bit(self):
        # Random int (0, bit)
        seed = 111

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
