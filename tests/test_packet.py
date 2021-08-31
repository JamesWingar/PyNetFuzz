"""
Unit tests for Packet class
"""
import unittest
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, UDP, TCP
from scapy.packet import Raw
from src import const
import src.exceptions as ex

# Modules under test
from src.packet import Packet
from src.packet import PacketDetails
from src.hosts import Host

# Testing the recursive sorting algorithms
class TestArgumentParser(unittest.TestCase):
    """ Testing Packet class and methods"""

    TCP_VALUE = const.TRANSPORT_PROTOCOLS_INFO['tcp']['value']
    UDP_VALUE = const.TRANSPORT_PROTOCOLS_INFO['udp']['value']

    def check_class_attributes(self, packet, test_target, test_source, test_packet_details):
        """ Method to check packet class attributes are correct"""
        self.assertEqual( # attributes
            (test_target, test_source, test_packet_details),
            (packet.target, packet.source, packet.details))
        self.assertEqual( # target
            (packet.target.ip, packet.target.mac, packet.target.port),
            (test_target.ip, test_target.mac, test_target.port))
        self.assertEqual( # source
            (packet.source.ip, packet.source.mac, packet.source.port),
            (test_source.ip, test_source.mac, test_source.port))
        # info
        self.assertEqual(packet.details.int_protocol, test_packet_details.int_protocol)
        self.assertEqual(packet.details.trans_protocol, test_packet_details.trans_protocol)
        self.assertEqual(packet.details.cast, test_packet_details.cast)
        self.assertEqual(packet.details.vlan, test_packet_details.vlan)
        self.assertEqual(packet.details.headers, test_packet_details.headers)
        self.assertEqual(packet.details.length, test_packet_details.length)
        if getattr(test_packet_details, 'ip_header', None):
            self.assertEqual(packet.details.ip_header, test_packet_details.ip_header)
        if getattr(test_packet_details, 'tcp_header', None):
            self.assertEqual(packet.details.tcp_header, test_packet_details.tcp_header)

    def check_packet_layers(self, packet, test_packet_details):
        """ Method to check packet layers are correct and present"""
        packet_layers = packet.packet.layers()
        self.assertTrue(Ether in packet_layers) # Ether layer
        self.assertTrue(IP in packet_layers) # IP layer
        if test_packet_details.trans_protocol == self.TCP_VALUE:
            self.assertTrue(TCP in packet_layers)
        elif test_packet_details.trans_protocol == self.UDP_VALUE:
            self.assertTrue(UDP in packet_layers)
        self.assertTrue(Raw in packet_layers)

    def check_packet_attributes(self, packet, test_target, test_source, test_packet_details):
        """ Method to check packet attributes are correct"""
        ether_layer = packet.packet.getlayer(Ether)
        self.assertEqual(
            (ether_layer.dst, ether_layer.src), (test_target.mac, test_source.mac))
        ip_layer = packet.packet.getlayer(IP)
        self.assertEqual(
            (ip_layer.dst, ip_layer.src), (test_target.ip, test_source.ip))
        if test_packet_details.trans_protocol == self.TCP_VALUE:
            trans_layer = packet.packet.getlayer(TCP)
        elif test_packet_details.trans_protocol == self.UDP_VALUE:
            trans_layer = packet.packet.getlayer(UDP)
        self.assertEqual(
            (trans_layer.dport, trans_layer.sport), (test_target.port, test_source.port))
        self.assertEqual(
            len(packet.packet.getlayer(Raw).load), test_packet_details.length)

    def test_valid_packet_ip4_tcp_headers(self):
        """ Test valid packet - Contains (IPv4, TCP, Headers)"""
        test_target_host = Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8080")
        test_source_host = Host("192.168.1.100", "99:00:A9:4F:3D:7E", "999")
        test_packet_details = PacketDetails({
            'int_protocol': 2048,
            'trans_protocol': 6,
            'cast': 'broadcast',
            'vlan': False,
            'headers': True,
            'length': 1454,
            'ip_header': {
                'ttl': 222, 'tos': 173, 'flags': 1, 'frag': 3557, 'id': 23671,},
            'tcp_header': {
                'seq': 1192725307, 'ack': 67273815, 'window': 53003, 'urgptr': 37447}})
        packet = Packet(test_target_host, test_source_host, test_packet_details)
        self.check_class_attributes(packet, test_target_host, test_source_host, test_packet_details)
        packet.add_all_layers()
        self.check_packet_layers(packet, test_packet_details)
        self.check_packet_attributes(packet, test_target_host,
            test_source_host, test_packet_details)

    def test_valid_packet_ip6_udp_headers(self):
        """ Test valid packet - Contains (IPv6, UDP, Headers)"""
        test_target_host = Host("255.255.255.255", "FF-FF-FF-FF-FF-FF", "65535")
        test_source_host = Host("0.0.0.0", "00:00:00:00:00:00", "1")
        test_packet_details = PacketDetails({
            'int_protocol': 34525,
            'trans_protocol': 17,
            'cast': 'unicast',
            'vlan': True,
            'headers': True,
            'length': 50,
            'ip_header': {'ttl': 123, 'tos': 154, 'flags': 0, 'frag': 4567, 'id': 20921,}})
        packet = Packet(test_target_host, test_source_host, test_packet_details)
        self.check_class_attributes(packet, test_target_host, test_source_host, test_packet_details)
        packet.add_all_layers()
        self.check_packet_layers(packet, test_packet_details)
        self.check_packet_attributes(packet, test_target_host,
            test_source_host, test_packet_details)

    def test_valid_packet_ip4_tcp(self):
        """ Test valid packet - Contains (IPv4, TCP, No Headers)"""
        test_target_host = Host("142.1.10.196", "4F:2E:22:0A:AA:BB", "1234")
        test_source_host = Host("97.100.0.0", "9F:12:11:74:A9:F1", "10000")
        test_packet_details = PacketDetails({
            'int_protocol': 2048,
            'trans_protocol': 6,
            'cast': 'multicast',
            'vlan': False,
            'headers': False,
            'length': 1499})
        packet = Packet(test_target_host, test_source_host, test_packet_details)
        self.check_class_attributes(packet, test_target_host, test_source_host, test_packet_details)
        packet.add_all_layers()
        self.check_packet_layers(packet, test_packet_details)
        self.check_packet_attributes(packet, test_target_host,
            test_source_host, test_packet_details)

    def test_valid_packet_ip6_udp(self):
        """ Test valid packet - Contains (IPv6, UDP, No Headers)"""
        test_target_host = Host("99.0.255.255", "00:12:67:99:0A:FF", "674")
        test_source_host = Host("9.1.1.123", "9F:12:11:74:A9:F1", "643")
        test_packet_details = PacketDetails({
            'int_protocol': 34525,
            'trans_protocol': 17,
            'cast': 'multicast',
            'vlan': False,
            'headers': False,
            'length': 1499})
        packet = Packet(test_target_host, test_source_host, test_packet_details)
        self.check_class_attributes(packet, test_target_host, test_source_host, test_packet_details)
        packet.add_all_layers()
        self.check_packet_layers(packet, test_packet_details)
        self.check_packet_attributes(packet, test_target_host,
            test_source_host, test_packet_details)

    def test_invalid_host(self):
        """ Test invalid host as a parameter to Packet class"""
        test_packet_details = PacketDetails({
            'int_protocol': 2048,
            'trans_protocol': 6,
            'cast': 'broadcast',
            'vlan': False,
            'headers': True,
            'length': 1454,
            'ip_header': {'ttl': 222, 'tos': 173, 'flags': 1, 'frag': 3557, 'id': 23671},
            'tcp_header': {'seq': 1192725307, 'ack': 67273815, 'window': 53003, 'urgptr': 37447}
        })

        with self.assertRaises(ex.HostNoIpAddressError):
            Packet(Host(None, "00:E7:EE:E7:61:5E", "8000"),
                Host("99.0.255.255", "00:12:67:99:0A:FF", "674"), test_packet_details)
        with self.assertRaises(ex.HostNoIpAddressError):
            Packet(Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                Host(None, "00:12:67:99:0A:FF", "674"), test_packet_details)
        with self.assertRaises(ex.HostNoMacAddressError):
            Packet(Host("192.168.1.1", None, "8000"),
                Host("99.0.255.255", "00:12:67:99:0A:FF", "674"), test_packet_details)
        with self.assertRaises(ex.HostNoMacAddressError):
            Packet(Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                Host("99.0.255.255", None, "674"), test_packet_details)
        with self.assertRaises(ex.HostNoPortAddressError):
            Packet(Host("192.168.1.1", "00:E7:EE:E7:61:5E", None),
                Host("99.0.255.255", "00:12:67:99:0A:FF", "674"), test_packet_details)
        with self.assertRaises(ex.HostNoPortAddressError):
            Packet(Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                Host("99.0.255.255", "00:12:67:99:0A:FF", None), test_packet_details)
        with self.assertRaises(ex.InvalidHostError):
            Packet("Test string",
                Host("99.0.255.255", "00:12:67:99:0A:FF", "674"), test_packet_details)
        with self.assertRaises(ex.InvalidHostError):
            Packet(Host("192.168.1.1", "00:E7:EE:E7:61:5E", "8000"),
                "Test string", test_packet_details)

        class Test():
            def __init__(self, test):
                self.test = test
        with self.assertRaises(ex.InvalidHostError):
            Packet(Test("test"), Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                test_packet_details,)
        with self.assertRaises(TypeError):
            Packet(Host(), Host("99.0.255.255", "00:12:67:99:0A:FF", "674"),
                test_packet_details,)

    def test_invalid_packet_info(self):
        """ Test invalid packet info as a parameter to Packet Details"""
        test_packet_details = PacketDetails({
            'int_protocol': 2048,
            'trans_protocol': 6,
            'cast': 'broadcast',
            'vlan': False,
            'headers': True,
            'length': 1454,
            'ip_header': { 'ttl': 222,'tos': 173,'flags': 1,'frag': 3557,'id': 23671,},
            'tcp_header': {'seq': 1192725307, 'ack': 67273815, 'window': 53003, 'urgptr': 37447},
        })

    def test_invalid_packet_info(self):
        """ Test invalid packet info as a parameter to Packet Details"""
        with self.assertRaises(ex.PacketInfoTypeError):
            PacketDetails("")
        with self.assertRaises(ex.PacketInfoTypeError):
            PacketDetails([])
        with self.assertRaises(ex.PacketInfoMissingEntriesError):
            PacketDetails({})
        with self.assertRaises(ex.PacketInfoMissingEntriesError):
            PacketDetails({'trans_protocol': 6, 'cast': 'broadcast', 'vlan': False,
                'headers': True, 'length': 1454})
        with self.assertRaises(ex.PacketInfoMissingEntriesError):
            PacketDetails({'int_protocol': 2048, 'cast': 'broadcast', 'vlan': False,
                'headers': True, 'length': 1454})
        with self.assertRaises(ex.PacketInfoMissingEntriesError):
            PacketDetails({'int_protocol': 2048, 'trans_protocol': 6, 'vlan': False,
                'headers': True, 'length': 1454})
        with self.assertRaises(ex.PacketInfoMissingEntriesError):
            PacketDetails({'int_protocol': 2048, 'trans_protocol': 6, 'cast': 'broadcast',
                'headers': True, 'length': 1454})
        with self.assertRaises(ex.PacketInfoMissingEntriesError):
            PacketDetails({'int_protocol': 2048, 'trans_protocol': 6, 'cast': 'broadcast',
                'vlan': False, 'length': 1454})

if __name__ == "__main__":
    unittest.main()
