CAST_TYPES = ('broadcast', 'multicast', 'unicast')
INTERNET_PROTOCOLS = ('ipv4', 'ipv6', 'jumbo')
TRANSPORT_PROTOCOLS = ('tcp', 'udp')

# Cast type values
CAST_TYPES_INFO = {
    'ipv4': {
        'multicast': {
            'IP': '224.0.0.1',
            'MAC': '01:00:5E:00:00:01',
        },
        'broadcast': {
            'IP': '255.255.255.255',
            'MAC': 'FF:FF:FF:FF:FF:FF',
        }
    },
    'ipv6': {
        'multicast': {
            'IP': 'FF02:0:0:0:0:0:0:1',
            'MAC': '33:33:00:00:00:01',
        },
    }
}

# Internet protocols (Ether types)
INTERNET_PROTOCOLS_INFO = {
    'ipv4': {
        'value': 0x800,
        'min_length': 60,
        'max_length': 1500,
    },
    'ipv6': {
        'value': 0x86DD,
        'min_length': 60,
        'max_length': 1500,
    },
    'jumbo': {
        'value': 0x8870,
        'min_length': 60,
        'max_length': 9000,
    }
}

# Transport protocols
TRANSPORT_PROTOCOLS_INFO = {
    'udp': {
        'value': 0x11,
    },
    'tcp': {
        'value': 0x06,
    }
}

# Constants
MAX_PORT = 65535

# Default values
DEFAULT_IP_ADDRESS = "192.168.1.0"
DEFAULT_MASK = 24
