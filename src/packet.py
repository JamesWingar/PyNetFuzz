# Python library imports
from typing import Any, Dict
from scapy.all import sendp, Ether, Dot1Q, IP, UDP, TCP, randstring
# Package imports
from src.hosts import Host
from src.const import (
    TRANSPORT_PROTOCOLS_INFO,
)
from src.validation import (
    valid_host,
    valid_packet_info,
    valid_packet_details,
)


class PacketDetails():

    def init(self, info: Dict):
        """ PacketDetails class built-in initialiser
   
        Parameters:
        info (Dict): dict containing packet required info  
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
        if type(attribute) is not str:
            raise TypeError(
                f'Attribute is not a string. Received: {attribute} ({type(attribute)})'
            )

        if getattr(self, attribute, None):
            return self.attribute
        return default


class Packet():

    def __init__(self, target: Host, source: Host, details: PacketDetails) -> None:
        """ Packet class built-in initialiser
   
        Parameters:
        target (Host): Target Host packet will be sent to 
        source (Host): Source Host packet will pretend to be from
        details (PacketDetails): Dictionary containing packet information
        """
        self.packet = None
        self.target = valid_host(target)
        self.source = valid_host(source)
        self.details = valid_packet_details(details)

    def add_ethernet_layer(self):
        """ Adds ethernet layer to packet attribute
   
        Returns:
        None: Returns None
        """
        self.packet = Ether(src=self.source.mac, dst=self.target.mac, type=self.details.int_protocol)
        if self.details.vlan:
            self.packet /= Dot1Q(vlan=True)
        return

    def add_ip_layer(self):
        """ Adds internet protocol layer to packet attribute
   
        Returns:
        None: Returns None
        """
        self.packet /= IP(src=self.source.ip, dst=self.target.ip)
        if self.details.headers:
            for key, value in self.details.ip_header.items():
                setattr(self.packet, key, value)
        return

    def add_transport_layer(self):
        """ Adds transport layer to packet attribute
   
        Returns:
        None: Returns None
        """
        if self.is_udp():
            self.packet /= UDP(sport=self.source.port, dport=self.target.port)
        elif self.is_tcp():
            self.packet /= TCP(sport=self.source.port, dport=self.target.port)
            if self.details.headers:
                for key, value in self.details.tcp_header.items():
                    setattr(self.packet, key, value)
        return

    def add_payload_layer(self):
        """ Adds random payload to packet attribute
   
        Returns:
        None: Returns None
        """
        self.packet /= randstring(self.details.length)
        return

    def add_all_layers(self):
        """ Adds all layers to packet attribute
   
        Returns:
        None: Returns None
        """
        self.add_ethernet_layer()
        self.add_ip_layer()
        self.add_transport_layer()
        self.add_payload_layer()
        return

    def send(self, iface, verbose=False):
        """ Sends packet attribute
   
        Returns:
        None: Returns None
        """
        sendp(self.packet, iface=iface, verbose=verbose)
        return
        
    def is_udp(self):
        """ Checks if transport protocol is UDP
   
        Returns:
        Bool: Boolean if transport protocol is UDP
        """
        return self.details.trans_protocol == TRANSPORT_PROTOCOLS_INFO['udp']['value']

    def is_tcp(self):
        """ Checks if transport protocol is TCP
   
        Returns:
        None: Boolean if transport protocol is TCP
        """
        return self.details.trans_protocol == TRANSPORT_PROTOCOLS_INFO['tcp']['value']

    def __str__(self):
        return f"Target:\n{self.target}\nSource:\n{self.source}\nInfo:\n" + \
            "\n".join([f"{key}: {self.details[key]}" for key in self.details])

    def repr(self):
        return f"Object: {self.__class__.__name__} ({repr(self.target)}, {repr(self.source)}, {(self.packet)}, {self.details})"
