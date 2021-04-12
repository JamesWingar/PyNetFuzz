import unittest
from src import arguments
from src import const
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


    def test_n_packets_arg(self):
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


    def test_MAC_arg(self):
        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tm', 'FF:FF:FF:FF:FF:FF', '-sm', 'FF:FF:FF:FF:FF:FF']
                )
        self.assertEqual((result.t_mac, result.s_mac), ('FF:FF:FF:FF:FF:FF', 'FF:FF:FF:FF:FF:FF'))

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tm', '00:00:00:00:00:00', '-sm', '00:00:00:00:00:00']
                )
        self.assertEqual((result.t_mac, result.s_mac), ('00:00:00:00:00:00', '00:00:00:00:00:00'))

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tm', '01:00:5E:00:00:01', '-sm', '01:00:5E:00:00:01']
                )
        self.assertEqual((result.t_mac, result.s_mac), ('01:00:5E:00:00:01', '01:00:5E:00:00:01'))

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tm', '33:33:00:00:00:01', '-sm', '33:33:00:00:00:01']
                )
        self.assertEqual((result.t_mac, result.s_mac), ('33:33:00:00:00:01', '33:33:00:00:00:01'))

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tm', '54:FE:9F:F9:AA:00', '-sm', '54:FE:9F:F9:AA:00']
                )
        self.assertEqual((result.t_mac, result.s_mac), ('54:FE:9F:F9:AA:00', '54:FE:9F:F9:AA:00'))

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tm', '54-FE-9F-F9-AA-00', '-sm', '54-FE-9F-F9-AA-00']
                )
        self.assertEqual((result.t_mac, result.s_mac), ('54-FE-9F-F9-AA-00', '54-FE-9F-F9-AA-00'))

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tm', '54FE.9FF9.AA00', '-sm', '54FE.9FF9.AA00']
                )
        self.assertEqual((result.t_mac, result.s_mac), ('54FE.9FF9.AA00', '54FE.9FF9.AA00'))

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tm', 'FG:FF:FF:FF:FF:FF', '-sm', 'FF:FG:FF:FF:FF:FF']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tm', 'GG:GG:GG:GG:GG:GG', '-sm', 'GG:GG:GG:GG:GG:GG']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tm', '01.9F:5E:00:66:01', '-sm', '09:9B:E7:C2:66:A1']
            )
        
        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tm', '01:9F:5E.00:66:01', '-sm', '09:9B:E7:C2:66:A1']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tm', '01:9F:5E:00:66:01', '-sm', '09:9B:E7:C2.66:A1']
            )


    def test_vlan_arg(self):
        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-vl']
                )
        self.assertEqual(result.vlan, True)

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000']
                )
        self.assertEqual(result.vlan, False)


    def test_internet_protocol_arg(self):
        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-ip', 'ipv4']
                )
        self.assertEqual(result.iprotocol, const.INTERNET_PROTOCOLS_INFO['ipv4']['value'])

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-ip', 'IPV4']
                )
        self.assertEqual(result.iprotocol, const.INTERNET_PROTOCOLS_INFO['ipv4']['value'])

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-ip', 'iPv4']
                )
        self.assertEqual(result.iprotocol, const.INTERNET_PROTOCOLS_INFO['ipv4']['value'])

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-ip', 'ipv6']
                )
        self.assertEqual(result.iprotocol, const.INTERNET_PROTOCOLS_INFO['ipv6']['value'])

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-ip', 'IPV6']
                )
        self.assertEqual(result.iprotocol, const.INTERNET_PROTOCOLS_INFO['ipv6']['value'])

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-ip', 'iPv6']
                )
        self.assertEqual(result.iprotocol, const.INTERNET_PROTOCOLS_INFO['ipv6']['value'])

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-ip', 'jumbo']
                )
        self.assertEqual(result.iprotocol, const.INTERNET_PROTOCOLS_INFO['jumbo']['value'])

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-ip', 'JUMBO']
                )
        self.assertEqual(result.iprotocol, const.INTERNET_PROTOCOLS_INFO['jumbo']['value'])

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-ip', 'jUmBo']
                )
        self.assertEqual(result.iprotocol, const.INTERNET_PROTOCOLS_INFO['jumbo']['value'])


    def test_transport_protocol_arg(self):
        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tp', 'udp']
                )
        self.assertEqual(result.tprotocol, const.TRANSPORT_PROTOCOLS_INFO['udp']['value'])

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tp', 'UDP']
                )
        self.assertEqual(result.tprotocol, const.TRANSPORT_PROTOCOLS_INFO['udp']['value'])

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tp', 'uDp']
                )
        self.assertEqual(result.tprotocol, const.TRANSPORT_PROTOCOLS_INFO['udp']['value'])

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tp', 'tcp']
                )
        self.assertEqual(result.tprotocol, const.TRANSPORT_PROTOCOLS_INFO['tcp']['value'])

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tp', 'TCP']
                )
        self.assertEqual(result.tprotocol, const.TRANSPORT_PROTOCOLS_INFO['tcp']['value'])

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-tp', 'tCp']
                )
        self.assertEqual(result.tprotocol, const.TRANSPORT_PROTOCOLS_INFO['tcp']['value'])


    def test_port_arg(self):
        result = arguments.parse_args(
                    ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-t_p', '2000', '-s_p', '4000']
                )
        self.assertEqual((result.t_port, result.s_port), (2000, 4000))

        result = arguments.parse_args(
                    ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-t_p', '1', '-s_p', '65535']
                )
        self.assertEqual((result.t_port, result.s_port), (1, 65535))

        result = arguments.parse_args(
                    ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-t_p', '65535', '-s_p', '1']
                )
        self.assertEqual((result.t_port, result.s_port), (65535, 1))

        
        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-t_p', '0', '-s_p', '65536']
            )
        
        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-t_p', '-1000', '-s_p', '8080']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-t_p', '8080', '-s_p', '-8080']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-t_p', '80', '-s_p', '655350']
            )
        

    def test_cast_arg(self):
        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-c', 'unicast']
                )
        self.assertEqual(result.cast, 'unicast')

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-c', 'UNICAST']
                )
        self.assertEqual(result.cast, 'unicast')

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-c', 'uNiCaSt']
                )
        self.assertEqual(result.cast, 'unicast')

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-c', 'multicast']
                )
        self.assertEqual(result.cast, 'multicast')

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-c', 'MULTICAST']
                )
        self.assertEqual(result.cast, 'multicast')

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-c', 'mUlTiCaSt']
                )
        self.assertEqual(result.cast, 'multicast')

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-c', 'broadcast']
                )
        self.assertEqual(result.cast, 'broadcast')

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-c', 'BROADCAST']
                )
        self.assertEqual(result.cast, 'broadcast')

        result = arguments.parse_args(
                    ['192.168.10.100', '192.168.12.50', 'eth0', '1000', '-c', 'bRoAdCaSt']
                )
        self.assertEqual(result.cast, 'broadcast')

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-c', '1000']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-c', 'br0adcast']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-c', 'dandelion']
            )


    def test_headers_arg(self):
        result = arguments.parse_args(
                    ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-hd']
                )
        self.assertEqual(result.headers, False)

        result = arguments.parse_args(
                    ['192.168.1.254', '192.168.1.10', 'eth0', '1000']
                )
        self.assertEqual(result.headers, True)


    def test_packet_length_arg(self):
        result = arguments.parse_args(
                    ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-min', '100', '-max', '7000']
                )
        self.assertEqual((result.min_packet, result.max_packet), (100, 7000))

        result = arguments.parse_args(
                    ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-min', '48', '-max', '9000']
                )
        self.assertEqual((result.min_packet, result.max_packet), (48, 9000))

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-min', '47', '-max', '9001']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-min', '-48', '-max', '8080']
            )

        with self.assertRaises(SystemExit) as exception:
            arguments.parse_args(
                ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-min', '300', '-max', '-9000']
            )


    def test_seed_arg(self):
        result = arguments.parse_args(
                    ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-s', '10000']
                )
        self.assertEqual(result.seed, 10000)

        result = arguments.parse_args(
                    ['192.168.1.254', '192.168.1.10', 'eth0', '1000', '-s', '1000000']
                )
        self.assertEqual(result.seed, 1000000)

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
