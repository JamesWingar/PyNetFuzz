# Python library imports
from scapy.all import sr1, IP, ICMP, getmacbyip
import psutil
# Package imports
import src.exceptions as ex
from src.validation import (
    valid_specific_IP,
    valid_scope_IP,
    valid_mac,
    valid_port,
    valid_name,
)


class Host():
    
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

        if self.interface:
            self.ip = self.get_local_ip(self.interface)
            self.mac = self.get_local_mac(self.interface)
        else:
            self.ip = valid_scope_IP(ip)
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

    def is_ip(self):
        """ Checks if IP is present

        Returns:
        bool: Returns true if IP is present
        """
        return self.ip != None

    def is_mac(self):
        """ Checks if MAC is present

        Returns:
        bool: Returns true if MAC is present
        """
        return self.mac != None

    def is_port(self):
        """ Checks if Port is present

        Returns:
        bool: Returns true if Port is present
        """
        return self.port != None

    def ping_host(self) -> bool:
        """ Pings host IP

        Returns:
        bool: Returns true if ping is successful
        """
        if not self.is_ip():
            raise ex.HostNoIpAddressError(
                f'Host has no IP address. You can not use '
                f'ping_host without an IP address.'
            )

        return sr1(
            IP(dst=self.ip) / ICMP(),
            timeout=1,
            verbose=False
        ) is not None

    def get_local_ip(self, iface: str) -> str:
        """ Gets IP address of local interface

        Parameters:
        iface (str): Name of the interface

        Returns:
        str: Uppercase string of the interface IP address
             (Returns '0.0.0.0' upon failure)
        """
        local_ifaces = psutil.net_if_addrs()
        if iface not in local_ifaces:
            raise ex.HostGetLocalIpError(
                f'Can not get local IP address. This could be '
                f'due to an incorrect interface name.'
            )
        return valid_specific_IP(local_ifaces[iface][0].address)

    def get_local_mac(self, iface: str) -> str:
        """ Gets MAC address of local interface
        
        Parameters:
        iface (str): Name of the interface

        Returns:
        str: Uppercase string of the local interface MAC address
        """
        local_ifaces = psutil.net_if_addrs()
        if iface not in local_ifaces:
            raise ex.HostGetLocalMacError(
                f'Can not get local Mac address. This could be '
                f'due to an incorrect interface name.'
            )
        return valid_mac(local_ifaces[iface][-1].address)

    def get_remote_mac(self, ip: str) -> str:
        """ Gets MAC address of a remote interface. Uses IP address of the class.
        
        Returns:
        str: Uppercase string of the remote interface MAC address
        """
        mac_addr = getmacbyip(ip).upper()
        if mac_addr is None:
            raise ex.HostGetRemoteMacError(
                f'Can not get remote Mac address. This could be '
                f'due to an incorrect IP address.'
            )
        return valid_mac(mac_addr)

    def __str__(self) -> str:
        return f"IP: {self.ip}, MAC: {self.mac}, Port: {self.port}, Interface: {self.interface}, Online: {self.online}"

    def __repr__(self) -> str:
        return f"Object: {self.__class__.__name__} ({self.ip}, {self.mac}, {self.port}, {self.interface}, {self.online})"