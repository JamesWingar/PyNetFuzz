import unittest
from src import arguments
import argparse

# Testing the recursive sorting algorithms
class TestArgumentParser(unittest.TestCase):
    
    def test_ip_arg(self):
        result = arguments.parse_args(
                    ['192.168.1.254', '192.168.1.10', 'eth0', '1000']
                )
        self.assertEqual((result.target_ip, result.source_ip), ('192.168.1.254', '192.168.1.10'))

        result = arguments.parse_args(
                    ['255.255.255.255', '255.255.255.255', 'eth0', '1000']
                )
        self.assertEqual((result.target_ip, result.source_ip), ('255.255.255.255', '255.255.255.255'))

        result = arguments.parse_args(
                    ['0.0.0.0', '0.0.0.0', 'eth0', '1000']
                )
        self.assertEqual((result.target_ip, result.source_ip), ('0.0.0.0', '0.0.0.0'))

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['256.255.255.255', '255.255.255.255', 'eth0', '1000']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['255.255.255.255', '256.255.255.255', 'eth0', '1000']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.1450', '255.255.255.255', 'eth0', '1000']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['255.255.255.255', '192.168.1.1450', 'eth0', '1000']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.1681.254', '192.168.1.254', 'eth0', '1000']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.1681.254', 'eth0', '1000']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192168.1.254', '192.168.1.254', 'eth0', '1000']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192168.1.254', 'eth0', '1000']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1254', '192.168.1.254', 'eth0', '1000']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.168.1254', 'eth0', '1000']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192-168-1-254', '192.168.1.254', 'eth0', '1000']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192-168-1-254', 'eth0', '1000']
            )
        
        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254/24', '192.168.1.254', 'eth0', '1000']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.168.1.254/24', 'eth0', '1000']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.-1.254', '192.168.1.254', 'eth0', '1000']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.168.-1.254', 'eth0', '1000']
            )
        
        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['', '192.168.-1.254', 'eth0', '1000']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '', 'eth0', '1000']
            )


    def test_interface_name_arg(self):

        result = arguments.parse_args(
                    ['192.168.1.254', '192.168.1.10', 'eth0', '1000']
                )
        self.assertEqual(result.network_interface, 'eth0')

        result = arguments.parse_args(
                    ['192.168.1.254', '192.168.1.10', 'enx39405730947563058235830583', '1000']
                )
        self.assertEqual(result.network_interface, 'enx39405730947563058235830583')

        result = arguments.parse_args(
                    ['192.168.1.254', '192.168.1.10', 'enx/[]#./.#;][;[/.', '1000']
                )
        self.assertEqual(result.network_interface, 'enx/[]#./.#;][;[/.')

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.168.1.10', '', '1000']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.168.1.10', 'enx394057309475630582358305831231', '1000']
            )

    def test_n_packets(self):
        result = arguments.parse_args(
                    ['192.168.1.254', '192.168.1.10', 'eth0', '10000']
                )
        self.assertEqual(result.n_packets, 10000)

        result = arguments.parse_args(
                    ['192.168.1.254', '192.168.1.10', 'eth0', '1000000']
                )
        self.assertEqual(result.n_packets, 1000000)

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.168.1.10', 'eth0', '0']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.168.1.10', 'eth0', '-10']
            )


if __name__ == "__main__":
    unittest.main()
