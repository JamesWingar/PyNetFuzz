from scapy.all import *
from src.randomiser import Randomiser
from src.hosts import Host
from src import const


class PacketGenerator():
    count = 0
    # Attribute

    # initialising
    def __init__(self, params, seed=int(time.time())):
        self.params = params
        self.seed = seed
        self.randomiser = Randomiser(seed)
        print(f"SEED: {seed}")


    def create_packet(self, target, source=Host(None, None, None)):
        
        #randomise hosts
        target, source = self.randomise_host(target), self.randomise_host(source)
        print(target)
        print(source)
        
        #randomise packet info
        packet_info = self.randomise_params(self.params)
        print(packet_info)

        #create packet
        packet = Packet(target, source, packet_info)
        print(packet)

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


    def randomise_params(self, params):
        packet_info = {
            'int_protocol': params['int_protocol'] if params['int_protocol'] else \
                const.INTERNET_PROTOCOLS_INFO[self.randomiser.choose(const.INTERNET_PROTOCOLS)]['value'],
            'trans_protocol': params['trans_protocol'] if params['trans_protocol'] else \
                const.TRANSPORT_PROTOCOLS_INFO[self.randomiser.choose(const.TRANSPORT_PROTOCOLS)]['value'],
            'cast': params['cast'] if params['cast'] else \
                self.randomiser.choose(const.CAST_TYPES),
            'vlan': params['vlan'],
            'headers': params['headers'],
        }

        if params['headers']:
            # Randomise IP header
            if packet_info['int_protocol'] == const.INTERNET_PROTOCOLS_INFO['ipv6']['value']:
                #ipv6
                packet_info['ip_header'] = {
                    'tc': self.randomiser.bit_8(), # Traffic class
                    'fl': self.randomiser.bit_8(), # Flow Label
                    'hlim': self.randomiser.bit_8(), # Identification
                }
            else:
                #ipv4 or jumbo 
                packet_info['ip_header'] = {
                    'ttl': self.randomiser.bit_8(), # TTL 
                    'tos': self.randomiser.bit_8(), # DSCP
                    'flags': self.randomiser.bit_2(), # Flags
                    'frag': self.randomiser.bit_13(), # Fragmentation offset
                    'id': self.randomiser.bit_16(), # Identification
                }

            # Random TCP header
            if packet_info['trans_protocol'] == const.TRANSPORT_PROTOCOLS_INFO['tcp']['value']:
                packet_info['tcp_header'] = {
                    'seq': self.randomiser.bit_32(), # sequence number (32 bit value)
                    'ack': self.randomiser.bit_32(), # Acknowledgment number (32 bit value)
                    'window': self.randomiser.bit_16(), # Window size (16 bit value)
                    'urgptr': self.randomiser.bit_16(), # urgent pointer (16 bit value)
                }

        return packet_info

    def get_count(self):
        return self.count


class Packet():

    def __init__(self, target, source, info):
        self.target = self.is_valid_host(target)
        self.source = self.is_valid_host(source)
        self.info = self.is_valid_info(info)

    def generate_ethernet_frame(self, info):
        """ 
        packet = Ether(src=args['smac'], dst=args['tmac'], type=args['type'])  # creates the packet (ethernet frame)
        if vlan:
            packet /= Dot1Q(vlan=vlan)
        """
        pass

    def generate_internet_protocol(self, info):
        """
        packet /= IP(src=args['sip'], dst=args['tip'])  # creates the packet (ethernet/IPv4)
        if header:
            randomise_ip_header(packet)  # randomise header variables
        """
        pass

    def generate_ip_header(self, info):
        """ 
        if is_ipv6(packet.type):
        packet.tc, packet.fl, packet.hlim = random.randint(0, 255), random.randint(0, 2**20), random.randint(0, 255)     # Traffic class, Flow Label, Identification
        elif is_ipv4(packet.type):
            packet.ttl, packet.tos, packet.flags = random.randint(0, 255), random.randint(0, 255), random.randint(0, 3)  # TTL, DSCP, Flags
            packet.frag, packet.id = random.randint(0, 8192), random.randint(0, 65536)  # Fragmentation offset, Identification
        """
        pass

    def generate_transport_protocol(self, info):
        """ 
        if is_udp(args):
            packet /= UDP(sport=args['sport'], dport=args['tport'])  # create udp layer
        elif is_tcp(args):
            packet /= TCP(sport=args['sport'], dport=args['tport'])  # create tcp layer
            if header:
                randomise_tcp_header(packet)  # randomise tcp header
        """
        pass

    def generate_payload(self, info):
        """ 
        if not min:
            min = ether_length[packet.type][0]
        if not max:
            max = ether_length[packet.type][1]
        payload = randstring(random.randint(min, max - 60))  # minus max IPv6 header and max TCP header (largest)
        return len(payload), packet / payload
        """
        pass

    def send(self):
        pass


    def is_valid_host(self, host):
        if not isinstance(host, Host):
            raise ValueError("Packet must have Target and Source as Host Class Objects\n Received: {}".format(host))
        
        if host.ip is None or host.mac is None or host.port is None:
            raise ValueError("Target and Source Host Objects cannot be None\n Received: {}".format(host))

        return host


    def is_valid_info(self, info):
        must_contain = ['int_protocol', 'trans_protocol', 'cast', 'vlan', 'headers', 'ip_header']
        for key in must_contain:
            if key not in info:
                raise KeyError("Packet info dict is missing: {}".format(key))

        if info['trans_protocol'] == const.TRANSPORT_PROTOCOLS_INFO['tcp']['value'] and 'tcp_header' not in info:
            raise KeyError("Packet info dict is missing: {}".format(key))
    
        return info


    def __str__(self):
        return f"Target:\n{self.target}\nSource:\n{self.source}\nInfo:\n" + \
            "\n".join([f"{key}: {self.info[key]}" for key in self.info])
    
