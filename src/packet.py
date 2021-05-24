from scapy.all import sendp, Ether, Dot1Q, IP, UDP, TCP, randstring
from time import time
from src.randomiser import Randomiser
from src.hosts import Host
from src import const


class PacketGenerator():
    # Class Attribute
    count = 0
    
    # initialising
    def __init__(self, params):
        self.params = params
        self.seed = params['seed'] if params['seed'] else int(time())
        self.randomiser = Randomiser(self.seed)
        # TODO: LOG seed as Randomiser
        print(f"SEED: {self.seed}")


    def create_packet(self, target, source=Host(None, None, None)):
        
        #randomise hosts
        target, source = self.randomise_host(target), self.randomise_host(source)
        
        #randomise packet info
        packet_info = self.randomise_params(self.params)
        print(f"PACKET INFO: {packet_info}")

        #create packet
        packet = Packet(target, source, packet_info).add_all_layers()
        
        # TODO: LOG Packet sent in concise way
        print(f"PACKET number {self.count}:\n{packet}")

        # increment created packet counter
        self.count += 1

        return packet


    def randomise_host(self, host, ip_str="*.*.*.*"):
        # Randomise host IP
        if host.is_ip():
            ip_str = host.ip
        host.ip = self.randomiser.ip(ip_str)
        # Randomise host MAC
        if not host.is_mac():
            host.mac = self.randomiser.mac()
        # Randomise host PORT
        if not host.is_port():
            host.port = self.randomiser.port()

        return host


    def randomise_params(self, params, min_len=0, max_len=None):

        int_str = self.randomiser.choose(const.INTERNET_PROTOCOLS)
        trans_str = self.randomiser.choose(const.TRANSPORT_PROTOCOLS)

        packet_info = {
            'int_protocol': params['int_protocol'] if params['int_protocol'] else \
                const.INTERNET_PROTOCOLS_INFO[int_str]['value'],
            'trans_protocol': params['trans_protocol'] if params['trans_protocol'] else \
                const.TRANSPORT_PROTOCOLS_INFO[trans_str]['value'],
            'cast': params['cast'] if params['cast'] else \
                self.randomiser.choose(const.CAST_TYPES),
            'vlan': params['vlan'],
            'headers': params['headers']
        }

        if not max_len:
            max_len = const.INTERNET_PROTOCOLS_INFO[int_str]['max_length'] - \
                const.INTERNET_PROTOCOLS_INFO[int_str]['header_length'] - \
                const.TRANSPORT_PROTOCOLS_INFO[trans_str]['header_length']

        packet_info['length'] = self.randomiser.rand(min_len, max_len)

        if params['headers']:
            # Randomise IP header
            if packet_info['int_protocol'] == const.INTERNET_PROTOCOLS_INFO['ipv6']['value']:
                #ipv6
                packet_info['ip_header'] = {
                    'tc': self.randomiser.bit_8(), # Traffic class
                    'fl': self.randomiser.bit_20(), # Flow Label
                    'hlim': self.randomiser.bit_8(), # Identification
                }
            else:
                #ipv4 or jumbo 
                packet_info['ip_header'] = {
                    'ttl': self.randomiser.bit_8(), # TTL 
                    'tos': self.randomiser.bit_8(), # DSCP
                    'flags': self.randomiser.bit_3(), # Flags
                    'frag': self.randomiser.bit_13(), # Fragmentation offset
                    'id': self.randomiser.bit_16(), # Identification
                }

            # Random TCP header
            if packet_info['trans_protocol'] == const.TRANSPORT_PROTOCOLS_INFO['tcp']['value']:
                packet_info['tcp_header'] = {
                    'seq': self.randomiser.bit_32(), # sequence number
                    'ack': self.randomiser.bit_32(), # Acknowledgment number
                    'window': self.randomiser.bit_16(), # Window size
                    'urgptr': self.randomiser.bit_16(), # urgent pointer
                }

        return packet_info

    def get_count(self):
        return self.count



class Packet():

    def __init__(self, target, source, info):
        self.packet = None
        self.target = self.is_valid_host(target)
        self.source = self.is_valid_host(source)
        self.info = self.is_valid_info(info)
        for key, value in info.items():
            setattr(self, key, value)


    # CLASS METHODS
    def add_ethernet_layer(self):
        self.packet = Ether(src=self.source.mac, dst=self.target.mac, type=self.int_protocol)
        if self.vlan:
            self.packet /= Dot1Q(vlan=True)
        return


    def add_ip_layer(self):
        self.packet /= IP(src=self.source.ip, dst=self.target.ip)
        if self.headers:
            for key, value in self.ip_header.items():
                setattr(self.packet, key, value)
        return


    def add_transport_layer(self):
        if self.is_udp():
            self.packet /= UDP(sport=self.source.port, dport=self.target.port)
        elif self.is_tcp():
            self.packet /= TCP(sport=self.source.port, dport=self.target.port)
            if self.headers:
                for key, value in self.tcp_header.items():
                    setattr(self.packet, key, value)
        return


    def add_payload_layer(self):
        self.packet /= randstring(self.length)
        return


    def add_all_layers(self):
        self.add_ethernet_layer()
        self.add_ip_layer()
        self.add_transport_layer()
        self.add_payload_layer()
        return


    def send(self, iface, verbose=False):
        sendp(self.packet, iface=iface, verbose=verbose)
        return
        
    
    # BOOLEAN METHODS
    def is_udp(self):
        return self.trans_protocol == const.TRANSPORT_PROTOCOLS_INFO['udp']['value']


    def is_tcp(self):
        return self.trans_protocol == const.TRANSPORT_PROTOCOLS_INFO['tcp']['value']


    # VALIDATION METHODS
    def is_valid_host(self, host):
        if not isinstance(host, Host):
            raise ValueError("Packet must have Target and Source as Host Class Objects\n Received: {}".format(host))
        
        if host.ip is None or host.mac is None or host.port is None:
            raise ValueError("Target and Source Host Objects cannot be None\n Received: {}".format(host))

        return host


    def is_valid_info(self, info):
        must_contain = ['int_protocol', 'trans_protocol', 'cast', 'length', 'vlan', 'headers']

        if info['headers']:
            must_contain.append('ip_header')
            if info['trans_protocol'] == const.TRANSPORT_PROTOCOLS_INFO['tcp']['value']:
                must_contain.append('tcp_header')

        if len(must_contain) != len(info):
            raise KeyError("Packet info received unexpected number of values")
    
        if set(must_contain) != set(info.keys()):
            if set(must_contain) - set(info.keys()):
                raise KeyError("Packet info has missing values: {}".format(set(must_contain) - set(info.keys())))
            if set(info.keys()) - set(must_contain):
                raise KeyError("Packet info has incorrect values: {}".format(set(info.keys()) - set(must_contain)))
        
        return info

    
    # BUILTIN METHODS
    def __str__(self):
        return f"Target:\n{self.target}\nSource:\n{self.source}\nInfo:\n" + \
            "\n".join([f"{key}: {self.info[key]}" for key in self.info])
    
