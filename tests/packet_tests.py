import unittest
from scapy.all import Ether, IP, UDP, TCP, Raw

from src import const
import src.exceptions as ex

# Module under test
from src.packet import Packet
from src.hosts import Host

# Constants
TCP_VALUE = const.TRANSPORT_PROTOCOLS_INFO['tcp']['value']
UDP_VALUE = const.TRANSPORT_PROTOCOLS_INFO['udp']['value']


# Testing the recursive sorting algorithms
class TestArgumentParser(unittest.TestCase):
    
    def check_class_attributes(self, packet, test_target, test_source, test_packet_info):
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


    def check_packet_layers(self, packet, test_packet_info):
        packet_layers = packet.packet.layers()
        # Ether layer
        self.assertTrue(Ether in packet_layers)
        # IP layer
        self.assertTrue(IP in packet_layers)
        # transport layer
        if test_packet_info['trans_protocol'] == TCP_VALUE:
            self.assertTrue(TCP in packet_layers)
        elif test_packet_info['trans_protocol'] == UDP_VALUE:
            self.assertTrue(UDP in packet_layers)
        # Payload layer
        self.assertTrue(Raw in packet_layers)


    def check_packet_attributes(self, packet, test_target, test_source, test_packet_info):
        # Ether layer
        ether_layer = packet.packet.getlayer(Ether)
        self.assertEqual(ether_layer.dst, test_target.mac)
        self.assertEqual(ether_layer.src, test_source.mac)
        # IP layer
        ip_layer = packet.packet.getlayer(IP)
        self.assertEqual(ip_layer.dst, test_target.ip)
        self.assertEqual(ip_layer.src, test_source.ip)
        # transport layer
        if test_packet_info['trans_protocol'] == TCP_VALUE:
            trans_layer = packet.packet.getlayer(TCP)
        elif test_packet_info['trans_protocol'] == UDP_VALUE:
            trans_layer = packet.packet.getlayer(UDP)
        self.assertEqual(trans_layer.dport, test_target.port)
        self.assertEqual(trans_layer.sport, test_source.port)
        # Payload layer
        self.assertEqual(len(packet.packet.getlayer(Raw).load), test_packet_info['length'])


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
        self.check_class_attributes(packet, test_target_host, test_source_host, test_packet_info)
        packet.add_all_layers()
        self.check_packet_layers(packet, test_packet_info)
        self.check_packet_attributes(packet, test_target_host, test_source_host, test_packet_info)


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
        self.check_class_attributes(packet, test_target_host, test_source_host, test_packet_info)
        packet.add_all_layers()
        self.check_packet_layers(packet, test_packet_info)
        self.check_packet_attributes(packet, test_target_host, test_source_host, test_packet_info)


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
        self.check_class_attributes(packet, test_target_host, test_source_host, test_packet_info)
        packet.add_all_layers()
        self.check_packet_layers(packet, test_packet_info)
        self.check_packet_attributes(packet, test_target_host, test_source_host, test_packet_info)


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
        self.check_class_attributes(packet, test_target_host, test_source_host, test_packet_info)
        packet.add_all_layers()
        self.check_packet_layers(packet, test_packet_info)
        self.check_packet_attributes(packet, test_target_host, test_source_host, test_packet_info)


    def test_invalid_host(self):
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

        with self.assertRaises(ex.HostNoIpAddressError) as exception:
            test_packet = Packet(
                    Host(None, "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    test_packet_info,
                ) 
        with self.assertRaises(ex.HostNoIpAddressError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host(None, "00:12:67:99:0A:FF", "674"),
                    test_packet_info,
                ) 
        with self.assertRaises(ex.HostNoMacAddressError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", None, "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    test_packet_info,
                ) 
        with self.assertRaises(ex.HostNoMacAddressError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", None, "674"),
                    test_packet_info,
                ) 
        with self.assertRaises(ex.HostNoPortAddressError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", None),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    test_packet_info,
                )
        with self.assertRaises(ex.HostNoPortAddressError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", None),
                    test_packet_info,
                )
        with self.assertRaises(ex.InvalidHostError) as exception:
            test_packet = Packet(
                    "Test string",
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    test_packet_info,
                )
        with self.assertRaises(ex.InvalidHostError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    "Test string",
                    test_packet_info,
                )

        class Test():
            def __init__(self, test):
                self.test = test

        with self.assertRaises(ex.InvalidHostError) as exception:
            test_packet = Packet(
                    Test("test"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    test_packet_info,
                )
        with self.assertRaises(ex.InvalidHostError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Test("test"),
                    test_packet_info,
                )
        with self.assertRaises(TypeError) as exception:
            test_packet = Packet(
                    Host(),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    test_packet_info,
                )
        with self.assertRaises(TypeError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host(),
                    test_packet_info,
                ) 


    def test_invalid_packet_info(self):
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

        with self.assertRaises(ex.PacketInfoTypeError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    "",
                )
        with self.assertRaises(ex.PacketInfoTypeError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    [],
                )
        with self.assertRaises(ex.PacketInfoKeysError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    {},
                )
        with self.assertRaises(ex.PacketInfoKeysError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    {
                        'trans_protocol': 6,
                        'cast': 'broadcast',
                        'vlan': False,
                        'headers': True,
                        'length': 1454,
                    },
                )
        with self.assertRaises(ex.PacketInfoKeysError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    {
                        'int_protocol': 2048,
                        'cast': 'broadcast',
                        'vlan': False,
                        'headers': True,
                        'length': 1454,
                    },
                )
        with self.assertRaises(ex.PacketInfoKeysError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    {
                        'int_protocol': 2048,
                        'trans_protocol': 6,
                        'vlan': False,
                        'headers': True,
                        'length': 1454,
                    },
                )
        with self.assertRaises(ex.PacketInfoKeysError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    {
                        'int_protocol': 2048,
                        'trans_protocol': 6,
                        'cast': 'broadcast',
                        'headers': True,
                        'length': 1454,
                    },
                )
        with self.assertRaises(ex.PacketInfoKeysError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    {
                        'int_protocol': 2048,
                        'trans_protocol': 6,
                        'cast': 'broadcast',
                        'vlan': False,
                        'length': 1454,
                    },
                )
        with self.assertRaises(ex.PacketInfoKeysError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    {
                        'int_protocol': 2048,
                        'trans_protocol': 6,
                        'cast': 'broadcast',
                        'vlan': False,
                        'headers': True,
                    },
                )
        with self.assertRaises(ex.PacketInfoLengthError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    {
                        'int_protocol': 2048,
                        'trans_protocol': 6,
                        'cast': 'broadcast',
                        'vlan': False,
                        'headers': True,
                        'length': 1454,
                    },
                )

        with self.assertRaises(ex.PacketInfoLengthError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    {
                        'int_protocol': 2048,
                        'trans_protocol': 6,
                        'cast': 'broadcast',
                        'vlan': False,
                        'headers': False,
                        'length': 1454,
                        'ip_header': {
                            'ttl': 222,
                            'tos': 173,
                            'flags': 1,
                            'frag': 3557,
                            'id': 23671,
                        },
                    },
                )
        with self.assertRaises(ex.PacketInfoLengthError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    {
                        'int_protocol': 2048,
                        'trans_protocol': 6,
                        'cast': 'broadcast',
                        'vlan': False,
                        'headers': False,
                        'length': 1454,
                        'tcp_header': {
                            'seq': 1192725307,
                            'ack': 67273815,
                            'window': 53003,
                            'urgptr': 37447
                        },
                    },
                )
        with self.assertRaises(ex.PacketInfoLengthError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    {
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
                    },
                )
        with self.assertRaises(ex.PacketInfoLengthError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    {
                        'int_protocol': 2048,
                        'trans_protocol': 17,
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
                    },
                )
        with self.assertRaises(ex.PacketInfoMissingEntriesError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    {
                        'int_protocol': 2048,
                        'trans_protocol': 6,
                        'cast': 'broadcast',
                        'vlan': False,
                        'headers': True,
                        'length': 1454,
                        'test': {
                        },
                        'tcp_header': {
                        },
                    },
                )
        with self.assertRaises(ex.PacketInfoMissingEntriesError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    {
                        'int_protocol': 2048,
                        'trans_protocol': 6,
                        'cast': 'broadcast',
                        'vlan': False,
                        'headers': True,
                        'length': 1454,
                        'ip_header': {
                        },
                        'test': {
                        },
                    },
                )
        with self.assertRaises(ex.PacketInfoMissingEntriesError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    {
                        'int_protocol': 2048,
                        'trans_protocol': 6,
                        'cast': 'broadcast',
                        'vlan': False,
                        'headers': True,
                        'length': 1454,
                        'test': {
                        },
                        'test2': {
                        },
                    },
                )
        with self.assertRaises(ex.PacketInfoMissingEntriesError) as exception:
            test_packet = Packet(
                    Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                    Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                    {
                        'int_protocol': 2048,
                        'trans_protocol': 17,
                        'cast': 'broadcast',
                        'vlan': False,
                        'headers': True,
                        'length': 1454,
                        'test': {
                        },
                    },
                )

if __name__ == "__main__":
    unittest.main()
