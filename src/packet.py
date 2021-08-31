"""
Contains packet related classes
- Packet (packet builder and object)
- PacketDetails (packet information storage class)
"""
# Python library imports
from typing import Any
from scapy.sendrecv import sendp
from scapy.layers.l2 import Ether, Dot1Q
from scapy.layers.inet import IP, UDP, TCP
from scapy.utils import randstring
# Package imports
from src.hosts import Host
from src.const import (
    TRANSPORT_PROTOCOLS_INFO,
)
from src.validation import (
    valid_host, valid_packet_info, valid_complete_packet_details
)


class PacketDetails():
    """ Storage class for required packet information"""

    def __init__(self, info: dict):
        """ PacketDetails class built-in initialiser

        Parameters:
            info (dict): dict containing packet required info
        """
        self.info = valid_packet_info(info)
        for key, value in info.items():
            setattr(self, key, value)

    def get(self, attribute: str, default: Any=None) -> Any:
        """ Attempts to get the requested attribute

        Parameters:
            attribute (str): attribute name to retrieve
            default (Any): fallback value should the attribute not exist

        Returns:
            Any: Returns value of the attribute, otherwise returns the default value
        """
        if not isinstance(attribute, str):
            raise TypeError(
                f'Attribute given is not a string. Received: {attribute} ({type(attribute)})')
        return getattr(self, attribute, default)

    def set(self, attribute: str, value: Any) -> Any:
        """ Attempts to set a attribute

        Parameters:
            attribute (str): attribute name to set
            value (Any): value of the attribute
        """
        if not isinstance(attribute, str):
            raise TypeError(
                f'Attribute given is not a string. Received: {attribute} ({type(attribute)})')
        setattr(self, attribute, value)

    def __str__(self) -> str:
        """Built-in str method"""
        return "({})".format(",".join([f"{key}: {value}" for key, value in self.info.items()]))

    def __repr__(self) -> str:
        """Built-in repr method"""
        return f"Object: {self.__class__.__name__} ({self.info})"


class Packet():
    """ Packet builder and utilities class"""

    def __init__(self, target: Host, source: Host, details: PacketDetails):
        """ Packet class built-in initialiser

        Parameters:
            target (Host): Target Host packet will be sent to
            source (Host): Source Host packet will pretend to be from
            details (PacketDetails): Dictionary containing packet information
        """
        self.packet = None
        self.target = valid_host(target)
        self.source = valid_host(source)
        self.details = valid_complete_packet_details(details)

    def add_ethernet_layer(self):
        """ Adds ethernet layer to packet attribute"""
        self.packet = Ether(
            src=self.source.mac, dst=self.target.mac, type=self.details.int_protocol)
        if self.details.vlan:
            self.packet /= Dot1Q(vlan=True)

    def add_ip_layer(self):
        """ Adds internet protocol layer to packet attribute"""
        self.packet /= IP(src=self.source.ip, dst=self.target.ip)
        if self.details.headers:
            for key, value in self.details.ip_header.items():
                setattr(self.packet, key, value)

    def add_transport_layer(self):
        """ Adds transport layer to packet attribute"""
        if self.is_udp():
            self.packet /= UDP(sport=self.source.port, dport=self.target.port)
        elif self.is_tcp():
            self.packet /= TCP(sport=self.source.port, dport=self.target.port)
            if self.details.headers:
                for key, value in self.details.tcp_header.items():
                    setattr(self.packet, key, value)

    def add_payload_layer(self):
        """ Adds random payload to packet attribute"""
        self.packet /= randstring(self.details.length)

    def add_all_layers(self):
        """ Adds all layers to packet attribute"""
        self.add_ethernet_layer()
        self.add_ip_layer()
        self.add_transport_layer()
        self.add_payload_layer()

    def send(self, iface, verbose=False):
        """ Sends packet attribute"""
        sendp(self.packet, iface=iface, verbose=verbose)

    def is_udp(self):
        """ Checks if transport protocol is UDP

        Returns:
            Bool: True if transport protocol is UDP
        """
        return self.details.trans_protocol == TRANSPORT_PROTOCOLS_INFO['udp']['value']

    def is_tcp(self):
        """ Checks if transport protocol is TCP

        Returns:
            Bool: True if transport protocol is TCP
        """
        return self.details.trans_protocol == TRANSPORT_PROTOCOLS_INFO['tcp']['value']

    def __str__(self) -> str:
        """Built-in str method"""
        return f"Target:({self.target})\nSource:({self.source})\nDetails:({self.details})"

    def repr(self) -> str:
        """Built-in repr method"""
        return f"Object: {self.__class__.__name__} ({repr(self.target)}, " \
            f"{repr(self.source)}, {repr(self.details)}, {(self.packet)})"
