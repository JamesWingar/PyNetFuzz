#Python library imports
from typing import Any
from time import time
import random
import re
# Package imports
from src.hosts import Host
from src.packet import PacketDetails 
from src.const import (
    REGEX_SPECIFIC_IP,
    REGEX_SCOPE_IP,
    REGEX_MAC,
    MAX_PORT,
    TRANSPORT_PROTOCOLS_INFO,
    CAST_TYPES,
    INTERNET_PROTOCOLS,
    TRANSPORT_PROTOCOLS,
    INTERNET_PROTOCOLS_INFO,
    PACKETS_PER_SEED,
)

from src.validation import (
    valid_scope_IP,
    valid_seed,
    valid_number,
)


class Randomiser():

    def __init__(self, seed: int=None) -> None:
        """ Randomiser class built-in initialiser
    
        Parameters:
        seed (int): Integer for Suedo-random numbers to be seed from
        """
        if not seed:
            seed = int(time())
        self.seed = valid_seed(seed)
        random.seed(seed)
    
    def ip(self, ip_str: str='*.*.*.*') -> str:
        """ Generate a randomised IP address string
   
        Parameters:
        ip_str (str): IP address string to randomise '*' characters
    
        Returns:
        str: Randomised IP address string
        """
        ip_str = valid_scope_IP(ip_str)

        return '.'.join([str(self.bit_8()) if byte == '*' else byte for byte in ip_str.split('.')])

    def mac(self) -> str:
        """ Generate a randomised MAC address string

        Returns:
        str: Randomised MAC address string
        """
        return '00:' + ':'.join([hex(self.bit_8()).lstrip('0x').upper() for octet in range(5)])

    def port(self) -> int:
        """ Generate a randomised Port number
    
        Returns:
        int: Randomised Port number (0, 65535)
        """
        return self.bit_16()

    def host(self, host: Host, random_host: Host) -> Host:
        """ Generate a randomised host from a given Host object
   
        Parameters:
        host (Host): Host object containing host info
        random_host (Host): Host object to be randomised
    
        Returns:
        random_host: Randomised Host object
        """
        random_host.ip = self.ip(host.ip) if host.is_ip() else self.ip()
        if not host.is_mac():
            random_host.mac = self.mac()
        if not host.is_port():
            random_host.port = self.port()

        return random_host

    def packet_details(self, details: PacketDetails, random_details: PacketDetails, min_length: int=0, max_length: int=None):
        """ Generate randomised packet details from a given PacketDetails object
   
        Parameters:
        details (PacketDetails): PacketDetails object containing given packet details
        random_details (PacketDetails): PacketDetails object to be randomised
        min_length (int): Minimum length of IP address
        max_length (int): Maximum length of IP address
    
        Returns:
        random_details (PacketDetails): Randomised PacketDetails object
        """
        int_str = self.choose(INTERNET_PROTOCOLS)
        trans_str = self.choose(TRANSPORT_PROTOCOLS)

        random_details.int_protocol = details.get(
            'int_protocol',
            INTERNET_PROTOCOLS_INFO[int_str]['value']
        )
        random_details.trans_protocol = details.get(
            'trans_protocol',
            TRANSPORT_PROTOCOLS_INFO[trans_str]['value']
        )
        random_details.cast = details.get(
            'cast',
            self.choose(CAST_TYPES)
        )
        random_details.vlan = details.get(
            'vlan', False
        )
        random_details.headers = details.get(
            'headers', False
        )

        if not min_length:
            min_length = 0
        if not max_length:
            max_length = INTERNET_PROTOCOLS_INFO[int_str]['max_length'] - \
                            INTERNET_PROTOCOLS_INFO[int_str]['header_length'] - \
                            TRANSPORT_PROTOCOLS_INFO[trans_str]['header_length']
        random_details.set('length', self.rand(min_length, max_length))

        if random_details.get('headers', None):
            # Randomise IP header
            if random_details.get('int_protocol') == INTERNET_PROTOCOLS_INFO['ipv6']['value']:
                random_details.set(
                    'ip_header',
                    { #ipv6
                        'tc': self.bit_8(), # Traffic class
                        'fl': self.bit_20(), # Flow Label
                        'hlim': self.bit_8(), # Identification
                    }
                )
            else:
                random_details.set(
                    'ip_header',
                    { #ipv4 or jumbo 
                        'ttl': self.bit_8(), # TTL 
                        'tos': self.bit_8(), # DSCP
                        'flags': self.bit_3(), # Flags
                        'frag': self.bit_13(), # Fragmentation offset
                        'id': self.bit_16(), # Identification
                    }
                )
            # Random TCP header
            if random_details.get('trans_protocol') == TRANSPORT_PROTOCOLS_INFO['tcp']['value']:
                random_details.set(
                    'tcp_header',
                    {
                    'seq': self.bit_32(), # sequence number
                    'ack': self.bit_32(), # Acknowledgment number
                    'window': self.bit_16(), # Window size
                    'urgptr': self.bit_16(), # urgent pointer
                    }
                )

        return random_details

    def boolean(self) -> bool:
        """ Generate a boolean value

        Returns:
        bool: Randomised boolean value
        """
        return random.randint(0, 1) == 1

    def index(self, length: int) -> int:
        """ Generate a randomised index from Length
   
        Parameters:
        length (int): Positive integer to randomise as max value
    
        Returns:
        int: Randomised integer from 0 to length parameter
        """
        length = valid_number(length, min=0)

        return random.randint(0, length - 1)

    def choose(self, choices: Any) -> Any:
        """ Randomised choice of value from a List
   
        Parameters:
        choices (Any): List of choices to return a value from
    
        Returns:
        Any: Randomised value from the List
        """
        if type(choices) not in [list, set, tuple, str]:
            raise TypeError('Choices argument must be an iterable.')
        if len(choices) < 1:
            raise ValueError('Choices argument must not be empty.')

        return choices[random.randint(0, len(choices) - 1)]

    def rand(self, min: int, max: int) -> int:
        """ Generate a randomised value between Min and Max
   
        Parameters:
        min (int): Value to use as a minimum boundary for randomising
        max (int): Value to use as a maximum boundary for randomising
    
        Returns:
        int: Randomised value between min and max boundaries
        """
        if not type(min) == int or not type(max) == int:
            raise TypeError('Min and Max must be an integer.')
        if min > max:
            raise ValueError('The minimum must be greater than the maximum.')
        
        return random.randint(min, max)

    def bit_32(self) -> int:
        """ Generate a randomised positive 32 bit value
    
        Returns:
        int: Randomised value between 0 and 32 bit
        """
        return random.randint(0, 2147483647)

    def bit_20(self) -> int:
        """ Generate a randomised positive 20 bit value
    
        Returns:
        int: Randomised value between 0 and 20 bit
        """
        return random.randint(0, 1048575)

    def bit_16(self) -> int:
        """ Generate a randomised positive 16 bit value
    
        Returns:
        int: Randomised value between 0 and 16 bit
        """
        return random.randint(0, 65535)

    def bit_13(self) -> int:
        """ Generate a randomised positive 13 bit value
    
        Returns:
        int: Randomised value between 0 and 13 bit
        """
        return random.randint(0, 8191)

    def bit_8(self) -> int:
        """ Generate a randomised positive 8 bit value
    
        Returns:
        int: Randomised value between 0 and 8 bit
        """
        return random.randint(0, 255)

    def bit_3(self) -> int:
        """ Generate a randomised positive 3 bit value
    
        Returns:
        int: Randomised value between 0 and 3 bit
        """
        return random.randint(0, 7)

    def bit_2(self) -> int:
        """ Generate a randomised positive 2 bit value
    
        Returns:
        int: Randomised value between 0 and 2 bit
        """
        return random.randint(0, 3)

    def __str__(self) -> str:
        return f'Randomiser - Seed: ({self.seed})'

    def __repr__(self) -> str:
        return f'Object: {self.__class__.__name__} ({self.seed})'
