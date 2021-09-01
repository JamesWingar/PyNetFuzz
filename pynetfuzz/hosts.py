"""
Contains Host class - object to store and interface with local and remote hosts
"""
# Python library imports
from scapy.sendrecv import sr1
from scapy.layers.l2 import getmacbyip
from scapy.layers.inet import IP, ICMP
import psutil
# Package imports
import pynetfuzz.exceptions as ex
from .validation import (
    valid_specific_ip, valid_scope_ip, valid_mac, valid_port, valid_name,
)


class Host():
    """ Class object interface to local and remote hosts"""

    def __init__(self, ip: str, mac: str, port: str, interface: str=None) -> None:
        """ Host class built-in initialiser

        Parameters:
            ip (str): IP address string
            mac (str): MAC address string
            port (str): Port value string
            interface (str): Optional argument for local interface name. If intereface
                is given the class will get local ip and mac addresses.
        """
        self.port = valid_port(port)
        self.interface = valid_name(interface)
        self.online = False

        if self.interface: # If interface given assumed local host
            self.ip = self.get_local_ip(self.interface)
            self.mac = self.get_local_mac(self.interface)
        else: # else assumed remote host
            self.ip = valid_scope_ip(ip)
            if mac == "self":
                self.mac = self.get_remote_mac(self.ip)
            else:
                self.mac = valid_mac(mac)

    def is_online(self) -> bool:
        """ Checks if host is online

        Returns:
            bool: Returns true if host is online
        """
        self.online = self.ping_host()
        return self.online

    def is_ip(self) -> bool:
        """ Checks if IP is present

        Returns:
            bool: Returns true if IP is present
        """
        return self.ip is not None

    def is_mac(self) -> bool:
        """ Checks if MAC is present

        Returns:
            bool: Returns true if MAC is present
        """
        return self.mac is not None

    def is_port(self) -> bool:
        """ Checks if Port is present

        Returns:
            bool: Returns true if Port is present
        """
        return self.port is not None

    def ping_host(self) -> bool:
        """ Pings host IP

        Returns:
            bool: Returns true if ping is successful
        """
        if not self.is_ip():
            raise ex.HostNoIpAddressError(
                'Host has no IP address. You can not use ping_host without an IP address.')

        return sr1(IP(dst=self.ip) / ICMP(), timeout=1, verbose=False) is not None

    @staticmethod
    def get_local_ip(iface: str) -> str:
        """ Gets IP address of local interface

        Parameters:
            iface (str): Name of the interface

        Returns:
            str: Uppercase string of the interface IP address (Returns '0.0.0.0' upon failure)
        """
        local_ifaces = psutil.net_if_addrs()
        if iface not in local_ifaces:
            raise ex.HostGetLocalIpError(
                'Can not get local IP address. Might be due to an incorrect interface name.')
        return valid_specific_ip(local_ifaces[iface][0].address)

    @staticmethod
    def get_local_mac(iface: str) -> str:
        """ Gets MAC address of local interface

        Parameters:
            iface (str): Name of the interface

        Returns:
            str: Uppercase string of the local interface MAC address
        """
        local_ifaces = psutil.net_if_addrs()
        if iface not in local_ifaces:
            raise ex.HostGetLocalMacError(
                'Can not get local Mac address. Might be due to an incorrect interface name.')
        return valid_mac(local_ifaces[iface][-1].address)

    @staticmethod
    def get_remote_mac(ip: str) -> str:
        """ Gets MAC address of a remote interface. Uses IP address of the class.

        Returns:
            str: Uppercase string of the remote interface MAC address
        """
        mac_addr = getmacbyip(ip).upper()
        if mac_addr is None:
            raise ex.HostGetRemoteMacError(
                'Can not get remote Mac address. Might be due to an incorrect IP address.')
        return valid_mac(mac_addr)

    def __str__(self) -> str:
        """Built-in str method"""
        return f"IP: {self.ip}, MAC: {self.mac}, Port: {self.port}, " \
            f"Interface: {self.interface}, Online: {self.online}"

    def __repr__(self) -> str:
        """Built-in repr method"""
        return f"Object: {self.__class__.__name__} ({self.ip}, {self.mac}, " \
            f"{self.port}, {self.interface}, {self.online})"
