# Python library imports
from typing import Dict
from scapy.all import sendp, Ether, Dot1Q, IP, UDP, TCP, randstring
# Package imports
from src.hosts import Host
from src.const import (
    TRANSPORT_PROTOCOLS_INFO,
)
from src.validation import (
    valid_host,
    valid_packet_info,
)


class Packet():

    def __init__(self, target: Host, source: Host, info: Dict) -> None:
        """ Packet class built-in initialiser
   
        Parameters:
        target (Host): Target Host packet will be sent to 
        source (Host): Source Host packet will pretend to be from
        info (Dict): Dictionary containing packet information
        """
        self.packet = None
        self.target = valid_host(target)
        self.source = valid_host(source)
        self.info = valid_packet_info(info)

        for key, value in info.items():
            setattr(self, key, value)

    def add_ethernet_layer(self):
        """ Adds ethernet layer to packet attribute
   
        Returns:
        None: Returns None
        """
        self.packet = Ether(src=self.source.mac, dst=self.target.mac, type=self.int_protocol)
        if self.vlan:
            self.packet /= Dot1Q(vlan=True)
        return

    def add_ip_layer(self):
        """ Adds internet protocol layer to packet attribute
   
        Returns:
        None: Returns None
        """
        self.packet /= IP(src=self.source.ip, dst=self.target.ip)
        if self.headers:
            for key, value in self.ip_header.items():
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
            if self.headers:
                for key, value in self.tcp_header.items():
                    setattr(self.packet, key, value)
        return

    def add_payload_layer(self):
        """ Adds random payload to packet attribute
   
        Returns:
        None: Returns None
        """
        self.packet /= randstring(self.length)
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
        None: Returns None
        """
        return self.trans_protocol == TRANSPORT_PROTOCOLS_INFO['udp']['value']


    def is_tcp(self):
        """ Checks if transport protocol is TCP
   
        Returns:
        None: Returns None
        """
        return self.trans_protocol == TRANSPORT_PROTOCOLS_INFO['tcp']['value']

    def __str__(self):
        return f"Target:\n{self.target}\nSource:\n{self.source}\nInfo:\n" + \
            "\n".join([f"{key}: {self.info[key]}" for key in self.info])

    def repr(self):
        return f"Object: {self.__class__.__name__} ({repr(self.target)}, {repr(self.source)}, {(self.packet)}, {self.info})"
    
