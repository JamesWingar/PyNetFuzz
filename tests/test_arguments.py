"""
Unit tests for argument parsing
"""
import unittest
from src import const

# Module under test
from src.arguments import parse_args

# Testing the Argument parser
class TestArgumentParser(unittest.TestCase):
    """Testing argument parsing methods and checking"""

    def test_valid_ip_arg(self):
        """Test valid ip argument parsing"""
        result = parse_args(['192.168.1.254', 'eth0', '1000', '-sip', '192.168.1.10'])
        self.assertEqual((result.target_ip, result.source_ip), ('192.168.1.254', '192.168.1.10'))
        result = parse_args(['255.255.255.255', 'eth0', '1000', '-sip', '255.255.255.255'])
        self.assertEqual((
            result.target_ip, result.source_ip), ('255.255.255.255', '255.255.255.255'))
        result = parse_args(['0.0.0.0', 'eth0', '1000', '-sip', '0.0.0.0'])
        self.assertEqual((result.target_ip, result.source_ip), ('0.0.0.0', '0.0.0.0'))
        result = parse_args(['10.10.10.10', 'eth0', '1000', '-sip', '192.168.*.45'])
        self.assertEqual((result.target_ip, result.source_ip), ('10.10.10.10', '192.168.*.45'))
        result = parse_args(['10.10.255.1', 'eth0', '1000', '-sip', '192.168.1.*'])
        self.assertEqual((result.target_ip, result.source_ip), ('10.10.255.1', '192.168.1.*'))
        result = parse_args(['0.0.0.0', 'eth0', '1000', '-sip', '0.0.0.*'])
        self.assertEqual((result.target_ip, result.source_ip), ('0.0.0.0', '0.0.0.*'))

    def test_invalid_ip_arg(self):
        """Test invalid ip argument parsing"""
        with self.assertRaises(SystemExit):
            parse_args(['256.255.255.255', 'eth0', '1000', '-sip', '255.255.255.255'])
        with self.assertRaises(SystemExit):
            parse_args(['255.255.255.255', 'eth0', '1000', '-sip', '256.255.255.255'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.1450', 'eth0', '1000', '-sip', '255.255.255.255'])
        with self.assertRaises(SystemExit):
            parse_args(['255.255.255.255', 'eth0', '1000', '-sip', '192.168.1.1450'])
        with self.assertRaises(SystemExit):
            parse_args(['192.1681.254', 'eth0', '1000', '-sip', '192.168.1.254'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'eth0', '1000', '-sip', '192.1681.254'])
        with self.assertRaises(SystemExit):
            parse_args(['192-168-1-254', 'eth0', '1000', '-sip', '192.168.1.254'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'eth0', '1000', '-sip', '192-168-1-254'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254/24', 'eth0', '1000', '-sip', '192.168.1.254'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'eth0', '1000', '-sip', '192.168.1.254/24'])
        with self.assertRaises(SystemExit):
            parse_args(['', 'eth0', '1000', '-sip', '192.168.1.254'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'eth0', '1000', '-sip', ''])

    def test_valid_interface_name_arg(self):
        """Test valid interface name argument parsing"""
        result = parse_args(['192.168.1.254', 'eth0', '1000'])
        self.assertEqual(result.network_interface, 'eth0')
        result = parse_args(['192.168.1.254', 'enx39405730947563058235830583', '1000'])
        self.assertEqual(result.network_interface, 'enx39405730947563058235830583')
        result = parse_args(['192.168.1.254', 'enx/[]#./.~<>#;!][;[/.', '1000'])
        self.assertEqual(result.network_interface, 'enx/[]#./.~<>#;!][;[/.')

    def test_invalid_interface_name_arg(self):
        """Test invalid interface name argument parsing"""
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', '', '1000'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'enx394057309475630582358305831231', '1000'])

    def test_valid_n_packets_arg(self):
        """Test valid number of packets argument parsing"""
        result = parse_args(['192.168.1.254', 'eth0', '10000'])
        self.assertEqual(result.n_packets, 10000)
        result = parse_args(['192.168.1.254', 'eth0', '1000000'])
        self.assertEqual(result.n_packets, 1000000)

    def test_invalid_n_packets_arg(self):
        """Test invalid number of packets argument parsing"""
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'eth0', '0'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'eth0', '-10'])

    def test_valid_mac_arg(self):
        """Test valid MAC address argument parsing"""
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-tm',
            'FF:FF:FF:FF:FF:FF', '-sm', 'FF:FF:FF:FF:FF:FF'])
        self.assertEqual(
            (result.target_mac, result.source_mac), ('FF:FF:FF:FF:FF:FF', 'FF:FF:FF:FF:FF:FF'))
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-tm',
            '00:00:00:00:00:00', '-sm', '00:00:00:00:00:00'])
        self.assertEqual(
            (result.target_mac, result.source_mac), ('00:00:00:00:00:00', '00:00:00:00:00:00'))
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-tm',
            '01:00:5E:00:00:01', '-sm', '01:00:5E:00:00:01'])
        self.assertEqual(
            (result.target_mac, result.source_mac), ('01:00:5E:00:00:01', '01:00:5E:00:00:01'))
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-tm',
            '33:33:00:00:00:01', '-sm', '33:33:00:00:00:01'])
        self.assertEqual(
            (result.target_mac, result.source_mac), ('33:33:00:00:00:01', '33:33:00:00:00:01'))
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-tm',
            '54:FE:9F:F9:AA:00', '-sm', '54:FE:9F:F9:AA:00'])
        self.assertEqual(
            (result.target_mac, result.source_mac), ('54:FE:9F:F9:AA:00', '54:FE:9F:F9:AA:00'))
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-tm',
            '54-FE-9F-F9-AA-00', '-sm', '54-FE-9F-F9-AA-00'])
        self.assertEqual(
            (result.target_mac, result.source_mac), ('54-FE-9F-F9-AA-00', '54-FE-9F-F9-AA-00'))
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-tm',
            '54FE.9FF9.AA00', '-sm', '54FE.9FF9.AA00'])
        self.assertEqual(
            (result.target_mac, result.source_mac), ('54FE.9FF9.AA00', '54FE.9FF9.AA00'))

    def test_invalid_mac_arg(self):
        """Test invalid MAC address argument parsing"""
        with self.assertRaises(SystemExit):
            parse_args(['192.168.10.100', 'eth0', '1000', '-tm',
                'FG:FF:FF:FF:FF:FF', '-sm', 'FF:FG:FF:FF:FF:FF'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.10.100', 'eth0', '1000', '-tm',
            'GG:GG:GG:GG:GG:GG', '-sm', 'GG:GG:GG:GG:GG:GG'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.10.100', 'eth0', '1000', '-tm',
                '01.9F:5E:00:66:01', '-sm', '09:9B:E7:C2:66:A1'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.10.100', 'eth0', '1000', '-tm',
                '01:9F:5E.00:66:01', '-sm', '09:9B:E7:C2:66:A1'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.10.100', 'eth0', '1000', '-tm',
                '01:9F:5E:00:66:01', '-sm', '09:9B:E7:C2.66:A1'])

    def test_vlan_arg(self):
        """Test vlan argument parsing"""
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-vl'])
        self.assertEqual(result.vlan, True)
        result = parse_args(['192.168.10.100', 'eth0', '1000'])
        self.assertEqual(result.vlan, False)

    def test_valid_internet_protocol_arg(self):
        """Test valid internet protocol argument parsing"""
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-ip', 'ipv4'])
        self.assertEqual(result.int_protocol, const.INTERNET_PROTOCOLS_INFO['ipv4']['value'])
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-ip', 'IPV4'])
        self.assertEqual(result.int_protocol, const.INTERNET_PROTOCOLS_INFO['ipv4']['value'])
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-ip', 'iPv4'])
        self.assertEqual(result.int_protocol, const.INTERNET_PROTOCOLS_INFO['ipv4']['value'])
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-ip', 'ipv6'])
        self.assertEqual(result.int_protocol, const.INTERNET_PROTOCOLS_INFO['ipv6']['value'])
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-ip', 'IPV6'])
        self.assertEqual(result.int_protocol, const.INTERNET_PROTOCOLS_INFO['ipv6']['value'])
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-ip', 'iPv6'])
        self.assertEqual(result.int_protocol, const.INTERNET_PROTOCOLS_INFO['ipv6']['value'])

        # Temporarily removed jumbo frames
        # result = parse_args(['192.168.10.100', 'eth0', '1000', '-ip', 'jumbo'])
        # self.assertEqual(result.int_protocol, const.INTERNET_PROTOCOLS_INFO['jumbo']['value'])
        # result = parse_args(['192.168.10.100', 'eth0', '1000', '-ip', 'JUMBO'])
        # self.assertEqual(result.int_protocol, const.INTERNET_PROTOCOLS_INFO['jumbo']['value'])
        # result = parse_args(['192.168.10.100', 'eth0', '1000', '-ip', 'jUmBo'])
        # self.assertEqual(result.int_protocol, const.INTERNET_PROTOCOLS_INFO['jumbo']['value'])

    def test_invalid_internet_protocol_arg(self):
        """Test invalid internet protocol argument parsing"""
        with self.assertRaises(SystemExit):
            parse_args(['192.168.10.100', 'eth0', '1000', '-ip', 'test'])

    def test_valid_transport_protocol_arg(self):
        """Test valid transport protocol argument parsing"""
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-tp', 'udp'])
        self.assertEqual(result.trans_protocol, const.TRANSPORT_PROTOCOLS_INFO['udp']['value'])
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-tp', 'UDP'])
        self.assertEqual(result.trans_protocol, const.TRANSPORT_PROTOCOLS_INFO['udp']['value'])
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-tp', 'uDp'])
        self.assertEqual(result.trans_protocol, const.TRANSPORT_PROTOCOLS_INFO['udp']['value'])
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-tp', 'tcp'])
        self.assertEqual(result.trans_protocol, const.TRANSPORT_PROTOCOLS_INFO['tcp']['value'])
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-tp', 'TCP'])
        self.assertEqual(result.trans_protocol, const.TRANSPORT_PROTOCOLS_INFO['tcp']['value'])
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-tp', 'tCp'])
        self.assertEqual(result.trans_protocol, const.TRANSPORT_PROTOCOLS_INFO['tcp']['value'])

    def test_invalid_transport_protocol_arg(self):
        """Test invalid transport protocol argument parsing"""
        with self.assertRaises(SystemExit):
            parse_args(['192.168.10.100', 'eth0', '1000', '-tp', 'test'])

    def test_valid_port_arg(self):
        """Test valid port number argument parsing"""
        result = parse_args(['192.168.1.254', 'eth0', '1000', '-t_p', '2000', '-s_p', '4000'])
        self.assertEqual((result.target_port, result.source_port), (2000, 4000))
        result = parse_args(['192.168.1.254', 'eth0', '1000', '-t_p', '1', '-s_p', '65535'])
        self.assertEqual((result.target_port, result.source_port), (1, 65535))
        result = parse_args(['192.168.1.254', 'eth0', '1000', '-t_p', '65535', '-s_p', '1'])
        self.assertEqual((result.target_port, result.source_port), (65535, 1))

    def test_invalid_port_arg(self):
        """Test invalid port number argument parsing"""
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'eth0', '1000', '-t_p', '65536', '-s_p', '0'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'eth0', '1000', '-t_p', '-1000', '-s_p', '8080'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'eth0', '1000', '-t_p', '80', '-s_p', '655350'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'eth0', '1000', '-t_p', '80', '-s_p', 'hello'])

    def test_valid_cast_arg(self):
        """Test valid cast type argument parsing"""
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-c', 'unicast'])
        self.assertEqual(result.cast, 'unicast')
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-c', 'UNICAST'])
        self.assertEqual(result.cast, 'unicast')
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-c', 'uNiCaSt'])
        self.assertEqual(result.cast, 'unicast')
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-c', 'multicast'])
        self.assertEqual(result.cast, 'multicast')
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-c', 'MULTICAST'])
        self.assertEqual(result.cast, 'multicast')
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-c', 'mUlTiCaSt'])
        self.assertEqual(result.cast, 'multicast')
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-c', 'broadcast'])
        self.assertEqual(result.cast, 'broadcast')
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-c', 'BROADCAST'])
        self.assertEqual(result.cast, 'broadcast')
        result = parse_args(['192.168.10.100', 'eth0', '1000', '-c', 'bRoAdCaSt'])
        self.assertEqual(result.cast, 'broadcast')

    def test_invalid_cast_arg(self):
        """Test invalid cast type argument parsing"""
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'eth0', '1000', '-c', '1000'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'eth0', '1000', '-c', 'br0adcast'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'eth0', '1000', '-c', 'dandelion'])

    def test_headers_arg(self):
        """Test headers argument parsing"""
        result = parse_args(['192.168.1.254', 'eth0', '1000', '-hd'])
        self.assertEqual(result.headers, False)
        result = parse_args(['192.168.1.254', 'eth0', '1000'])
        self.assertEqual(result.headers, True)

    def test_valid_packet_length_arg(self):
        """Test valid packet length argument parsing"""
        result = parse_args(['192.168.1.254', 'eth0', '1000', '-min', '100', '-max', '7000'])
        self.assertEqual((result.min_length, result.max_length), (100, 7000))
        result = parse_args(['192.168.1.254', 'eth0', '1000', '-min', '48', '-max', '9000'])
        self.assertEqual((result.min_length, result.max_length), (48, 9000))

    def test_invalid_packet_length_arg(self):
        """Test invalid packet length argument parsing"""
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'eth0', '1000', '-min', '47', '-max', '9001'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'eth0', '1000', '-min', '-48', '-max', '8080'])

    def test_valid_seed_arg(self):
        """Test valid seed argument parsing"""
        result = parse_args(['192.168.1.254', 'eth0', '1000', '-s', '10000'])
        self.assertEqual(result.seed, 10000)
        result = parse_args(['192.168.1.254', 'eth0', '1000', '-s', '1000000'])
        self.assertEqual(result.seed, 1000000)

    def test_invalid_seed_arg(self):
        """Test invalid seed argument parsing"""
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'eth0', '1000', '-s', '0'])
        with self.assertRaises(SystemExit):
            parse_args(['192.168.1.254', 'eth0', '1000', '-s', '-10'])

if __name__ == "__main__":
    unittest.main()
