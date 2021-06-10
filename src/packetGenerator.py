#Python library imports

# Package imports
from src.randomiser import Randomiser
from src.packet import Packet
from src.hosts import Host
from src.const import (
    CAST_TYPES,
    INTERNET_PROTOCOLS,
    TRANSPORT_PROTOCOLS,
    INTERNET_PROTOCOLS_INFO,
    TRANSPORT_PROTOCOLS_INFO,
)

class PacketGenerator():
    # Class Attribute
    count = 0
    
    # initialising
    def __init__(self, params):
        self.params = params
        if params['seed']:
            self.randomiser = Randomiser(params['seed'])
        else:
            self.randomiser = Randomiser()
        self.seed = self.randomiser.seed

        # TODO: LOG seed as Randomiser
        print(f"SEED: {self.seed}")


    def create_packet(self, target, source=Host(None, None, None)):
        
        #randomise hosts
        target, source = self.randomise_host(target), self.randomise_host(source)
        
        #randomise packet info
        packet_info = self.randomise_params(self.params)
        print(f"PACKET INFO: {packet_info}")

        #create packet
        packet = Packet(target, source, packet_info)
        packet.add_all_layers()
        
        # TODO: LOG Packet sent in concise way
        print(f"PACKET number {self.count}:\n{packet}")

        # increment created packet counter
        self.count += 1

        return packet


    def randomise_host(self, host):
        # Randomise host IP
        if host.is_ip():
            host.ip = self.randomiser.ip(host.ip)
        else:
            host.ip = self.randomiser.ip()

        # Randomise host MAC
        if not host.is_mac():
            host.mac = self.randomiser.mac()
        # Randomise host PORT
        if not host.is_port():
            host.port = self.randomiser.port()

        return host


    def randomise_params(self, params, min_len=0, max_len=None):

        int_str = self.randomiser.choose(INTERNET_PROTOCOLS)
        trans_str = self.randomiser.choose(TRANSPORT_PROTOCOLS)

        packet_info = {
            'int_protocol': params['int_protocol'] if params['int_protocol'] else \
                INTERNET_PROTOCOLS_INFO[int_str]['value'],
            'trans_protocol': params['trans_protocol'] if params['trans_protocol'] else \
                TRANSPORT_PROTOCOLS_INFO[trans_str]['value'],
            'cast': params['cast'] if params['cast'] else \
                self.randomiser.choose(CAST_TYPES),
            'vlan': params['vlan'],
            'headers': params['headers']
        }

        if not max_len:
            max_len = INTERNET_PROTOCOLS_INFO[int_str]['max_length'] - \
                INTERNET_PROTOCOLS_INFO[int_str]['header_length'] - \
                TRANSPORT_PROTOCOLS_INFO[trans_str]['header_length']

        packet_info['length'] = self.randomiser.rand(min_len, max_len)

        if params['headers']:
            # Randomise IP header
            if packet_info['int_protocol'] == INTERNET_PROTOCOLS_INFO['ipv6']['value']:
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
            if packet_info['trans_protocol'] == TRANSPORT_PROTOCOLS_INFO['tcp']['value']:
                packet_info['tcp_header'] = {
                    'seq': self.randomiser.bit_32(), # sequence number
                    'ack': self.randomiser.bit_32(), # Acknowledgment number
                    'window': self.randomiser.bit_16(), # Window size
                    'urgptr': self.randomiser.bit_16(), # urgent pointer
                }

        return packet_info

    def get_count(self):
        return self.count