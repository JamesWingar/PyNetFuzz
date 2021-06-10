import unittest
from src import const

# Module under test
from src.packet import Packet
from src.hosts import Host


# Testing the recursive sorting algorithms
class TestArgumentParser(unittest.TestCase):
    

    def check_attributes(self, packet, test_target, test_source, test_packet_info):
        # attributes
        self.assertEqual(packet.target, test_target)
        self.assertEqual(packet.source, test_source)
        self.assertEqual(packet.info, test_packet_info)
        # target
        self.assertEqual(packet.target.ip, test_target.ip)
        self.assertEqual(packet.target.mac, test_target.mac)
        self.assertEqual(packet.target.port, test_target.port)
        # source
        self.assertEqual(packet.source.ip, test_source.ip)
        self.assertEqual(packet.source.mac, test_source.mac)
        self.assertEqual(packet.source.port, test_source.port)
        # info
        self.assertEqual(packet.int_protocol, test_packet_info['int_protocol'])
        self.assertEqual(packet.trans_protocol, test_packet_info['trans_protocol'])
        self.assertEqual(packet.cast, test_packet_info['cast'])
        self.assertEqual(packet.vlan, test_packet_info['vlan'])
        self.assertEqual(packet.headers, test_packet_info['headers'])
        self.assertEqual(packet.length, test_packet_info['length'])
        if 'ip_header'in test_packet_info:
            self.assertEqual(packet.ip_header, test_packet_info['ip_header'])
        if 'tcp_header' in test_packet_info:
            self.assertEqual(packet.tcp_header, test_packet_info['tcp_header'])


    def test_valid_params_ip4_tcp_headers(self):
        test_target_host = Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8080")
        test_source_host = Host("192.168.1.100", "99:00:A9:4F:3D:7E", "999")

        test_packet_info = {
            'int_protocol': 2048,
            'trans_protocol': 6,
            'cast': 'broadcast',
            'vlan': False,
            'headers': True,
            'length': 1454,
            'ip_header': {
                'ttl': 222,
                'tos': 173,
                'flags': 1,
                'frag': 3557,
                'id': 23671,
            },
            'tcp_header': {
                'seq': 1192725307,
                'ack': 67273815,
                'window': 53003,
                'urgptr': 37447
            },
        }

        packet = Packet(test_target_host, test_source_host, test_packet_info)
        self.check_attributes(packet, test_target_host, test_source_host, test_packet_info)
        packet.add_all_layers()
        # Add check for layers

    def test_valid_params_ip6_udp_headers(self):
        test_target_host = Host("255.255.255.255", "FF-FF-FF-FF-FF-FF", "65535")
        test_source_host = Host("0.0.0.0", "00:00:00:00:00:00", "1")

        test_packet_info = {
            'int_protocol': 34525,
            'trans_protocol': 17,
            'cast': 'unicast',
            'vlan': True,
            'headers': True,
            'length': 50,
            'ip_header': {
                'ttl': 123,
                'tos': 154,
                'flags': 0,
                'frag': 4567,
                'id': 20921,
            },
        }

        packet = Packet(test_target_host, test_source_host, test_packet_info)
        self.check_attributes(packet, test_target_host, test_source_host, test_packet_info)
        packet.add_all_layers()
        # Add check for layers

    def test_valid_params_ip4_tcp(self):
        test_target_host = Host("142.1.10.196", "4F:2E:22:0A:AA:BB", "1234")
        test_source_host = Host("97.100.0.0", "9F:12:11:74:A9:F1", "10000")

        test_packet_info = {
            'int_protocol': 2048,
            'trans_protocol': 6,
            'cast': 'multicast',
            'vlan': False,
            'headers': False,
            'length': 1499,
        }

        packet = Packet(test_target_host, test_source_host, test_packet_info)
        self.check_attributes(packet, test_target_host, test_source_host, test_packet_info)
        packet.add_all_layers()
        # Add check for layers

    def test_valid_params_ip6_udp(self):
        test_target_host = Host("99.0.255.255", "00:12:67:99:0A:FF", "674")
        test_source_host = Host("9.1.1.123", "9F:12:11:74:A9:F1", "643")

        test_packet_info = {
            'int_protocol': 34525,
            'trans_protocol': 17,
            'cast': 'multicast',
            'vlan': False,
            'headers': False,
            'length': 1499,
        }

        packet = Packet(test_target_host, test_source_host, test_packet_info)
        self.check_attributes(packet, test_target_host, test_source_host, test_packet_info)
        packet.add_all_layers()
        # Add check for layers


    def test_invalid_parameters(self):
        pass
    

if __name__ == "__main__":
    unittest.main()
