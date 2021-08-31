"""
Unit tests for Host class
"""
import unittest
import socket
import psutil
import src.exceptions as ex

# Module under test
from src.hosts import Host

# Testing the Host Class
class TestArgumentParser(unittest.TestCase):
    """ Testing Host class and methods"""

    @staticmethod
    def get_test_interface_info():
        """ Static method for getting local interface IP and MAC

        Returns:
            tuple: Details of a local interface (name, ip, mac)
        """ 
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        ifaces = psutil.net_if_addrs()
        for iface_name, iface_info in ifaces.items():
            if iface_info[0].address == ip_address:
                return (
                    iface_name,
                    iface_info[0].address,
                    iface_info[-1].address.upper(),
                )
        return False

    def test_valid_parameters(self):
        """ Test valid parameters initialising"""
        test_host = Host("0.168.1.1", "00:E7:EE:E7:61:5E", "8000")
        self.assertEqual(
            (test_host.ip_addr, test_host.mac, test_host.port, test_host.online),
            ("0.168.1.1", "00:E7:EE:E7:61:5E", 8000, False))
        test_host = Host("255.45.1.*", "FF:FF:FF:FF:FF:FF", "1")
        self.assertEqual(
            (test_host.ip_addr, test_host.mac, test_host.port, test_host.online),
            ("255.45.1.*", "FF:FF:FF:FF:FF:FF", 1, False))
        test_host = Host("192.99.*.*", "00:00:00:00:00:00", 65535.0)
        self.assertEqual(
            (test_host.ip_addr, test_host.mac, test_host.port, test_host.online),
            ("192.99.*.*", "00:00:00:00:00:00", 65535, False))
        test_host = Host("1.*.*.*", "AF:AF:AF:AF:AF:AF", 43231)
        self.assertEqual(
            (test_host.ip_addr, test_host.mac, test_host.port, test_host.online),
            ("1.*.*.*", "AF:AF:AF:AF:AF:AF", 43231, False))
        test_host = Host("*.*.*.*", "99:00:A9:4F:3D:7E", "12645")
        self.assertEqual(
            (test_host.ip_addr, test_host.mac, test_host.port, test_host.online),
            ("*.*.*.*", "99:00:A9:4F:3D:7E", 12645, False))
        test_host = Host(None, None, None)
        self.assertEqual(
            (test_host.ip_addr, test_host.mac, test_host.port, test_host.online),
            (None, None, None, False))

    def test_invalid_ip(self):
        """ Test invalid ip address parameter"""
        with self.assertRaises(ex.IpScopeAddressInvalidFormatError):
            Host('256.255.255.255', "00:E7:EE:E7:61:5E", "8000")
        with self.assertRaises(ex.IpScopeAddressInvalidFormatError):
            Host('192.168.1.1450', "00:E7:EE:E7:61:5E", "8000")
        with self.assertRaises(ex.IpScopeAddressInvalidFormatError):
            Host('192168.1.254', "00:E7:EE:E7:61:5E", "8000")
        with self.assertRaises(ex.IpScopeAddressInvalidFormatError):
            Host('192.168.1254', "00:E7:EE:E7:61:5E", "8000")
        with self.assertRaises(ex.IpScopeAddressInvalidFormatError):
            Host('192-168-1-254', "00:E7:EE:E7:61:5E", "8000")
        with self.assertRaises(ex.IpScopeAddressInvalidFormatError):
            Host('192.168.1.254/24', "00:E7:EE:E7:61:5E", "8000")
        with self.assertRaises(ex.IpAddressTooShortValueError):
            Host("", "00:E7:EE:E7:61:5E", "8000")

    def test_invalid_mac(self):
        """ Test invalid mac address parameter"""
        with self.assertRaises(ex.MacAddressInvalidFormatError):
            Host("192.99.1.10", 'FG:FF:FF:FF:FF:FF', "8000")
        with self.assertRaises(ex.MacAddressInvalidFormatError):
            Host("192.99.1.10", 'GG:GG:GG:GG:GG:GG', "8000")
        with self.assertRaises(ex.MacAddressInvalidFormatError):
            Host("192.99.1.10", '01:9F:5E.00:66:01', "8000")
        with self.assertRaises(ex.MacAddressInvalidFormatError):
            Host("192.99.1.10", '01:9F:5E/00:66:01', "8000")
        with self.assertRaises(ex.MacAddressInvalidFormatError):
            Host("192.99.1.10", "00:E7:EE:E7:615E", "8000")
        with self.assertRaises(ex.MacAddressInvalidFormatError):
            Host("192.99.1.10", "00:E7:EE:E7:61", "8000")
        with self.assertRaises(ex.MacAddressTooShortValueError):
            Host("192.99.1.10", "", "8000")

    def test_invalid_port(self):
        """ Test invalid port parameter"""
        with self.assertRaises(ex.PortInvalidValueError):
            Host("192.99.1.10", "00:E7:EE:E7:61:5E", "65536")
        with self.assertRaises(ex.PortInvalidValueError):
            Host("192.99.1.10", "00:E7:EE:E7:61:5E", "-1000")
        with self.assertRaises(ex.PortInvalidValueError):
            Host("192.99.1.10", "00:E7:EE:E7:61:5E", "0")
        with self.assertRaises(ex.PortInvalidFormatError):
            Host("192.99.1.10", "00:E7:EE:E7:61:5E", "hello")
        with self.assertRaises(ex.PortInvalidFormatError):
            Host("192.99.1.10", "00:E7:EE:E7:61:5E", "234.1")
        with self.assertRaises(ex.PortInvalidFormatError):
            Host("192.99.1.10", "00:E7:EE:E7:61:5E", "")

    def test_invalid_interface(self):
        """ Test invalid interface name parameter"""
        with self.assertRaises(ex.NameInvalidTypeError):
            Host("192.99.1.10", "00:E7:EE:E7:61:5E", "8000", [])
        with self.assertRaises(ex.NameInvalidTypeError):
            Host("192.99.1.10", "00:E7:EE:E7:61:5E", "8000", 12039)
        with self.assertRaises(ex.NameTooShortError):
            Host("192.99.1.10", "00:E7:EE:E7:61:5E", "8000", "")
        with self.assertRaises(ex.NameTooLongError):
            Host("192.99.1.10", "00:E7:EE:E7:61:5E", "8000", "abcdefghijklmnopqrstuvwxyz123456")
        with self.assertRaises(ex.HostGetLocalIpError):
            Host("192.99.1.10", "00:E7:EE:E7:61:5E", "8000", "hello")

    def test_valid_get_local_host(self):
        """ Test valid get local host method"""
        (iface_name, iface_addr, iface_mac) = self.get_test_interface_info()

        test_host = Host(iface_addr, "self", "8080", iface_name)
        self.assertEqual(
            (test_host.ip_addr, test_host.mac, test_host.port, test_host.online),
            (iface_addr, iface_mac, 8080, False))
        test_host = Host(iface_addr, iface_mac, 8080, iface_name)
        self.assertEqual(
            (test_host.ip_addr, test_host.mac, test_host.port, test_host.online),
            (iface_addr, iface_mac, 8080, False))
        test_host = Host(iface_addr, "00:00:00:00:00:00", "8080", iface_name)
        self.assertEqual(
            (test_host.ip_addr, test_host.mac, test_host.port, test_host.online),
            (iface_addr, iface_mac, 8080, False))
        test_host = Host("192.168.1.1", None, None, iface_name)
        self.assertEqual(
            (test_host.ip_addr, test_host.mac, test_host.port, test_host.online),
            (iface_addr, iface_mac, None, False))
        test_host = Host(None, None, None, iface_name)
        self.assertEqual(
            (test_host.ip_addr, test_host.mac, test_host.port, test_host.online),
            (iface_addr, iface_mac, None, False))

    def test_invalid_get_local_host(self):
        """ Test invalid get local host method"""
        (_, iface_addr, _) = self.get_test_interface_info()

        with self.assertRaises(ex.HostGetLocalIpError):
            Host(iface_addr, "self", "8080", "hello")


if __name__ == "__main__":
    unittest.main()
