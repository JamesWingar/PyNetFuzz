"""
Methods for parsing command line arguments with argument check methods
"""
# Python library imports
import argparse
import re
# Package imports
from .const import (
    REGEX_SPECIFIC_IP, REGEX_SCOPE_IP, REGEX_MAC,
    INTERNET_PROTOCOLS, INTERNET_PROTOCOLS_INFO,
    TRANSPORT_PROTOCOLS, TRANSPORT_PROTOCOLS_INFO,
    MAX_PORT, CAST_TYPES, 
)


def parse_args(args=None):
    """Build and parse command line positional and optional arguments and returns as a Namespace.

    Returns:
        Class: Argparse namespace class with command line arguments.
    """

    parser = argparse.ArgumentParser(
        prog='Network Fuzzing',
        usage='\n[Filename] %(prog)s \n[Positional arguments] <target IP> ' \
            '<Network interface> <N packets> \n[Optional arguments] [source_ip' \
            ' | target_mac | source_mac | target_port | source_port | ' \
            'int_protocol | trans_protocol | cast | headers | vlan | min_packet' \
            ' | max_packet | seed]',
        description='Creates and sends suedo-random network packets as part of a Fuzz Test.',
        epilog='For more detail go to the ReadMe file in main directory.')

    # Positional arguments
    parser.add_argument('target_ip', help='IP address of target on network',
        type=check_arg_specific_ip)
    parser.add_argument('network_interface',
        help='Name of the interface connected to the local network', type=check_arg_name)
    parser.add_argument(
        'n_packets', help='Number of packets to be sent', type=check_arg_positive_int)

    # Optional arguments
    parser.add_argument('-sip', '--source_ip',
        help='IP address of source on network (default: Random)',
        type=check_arg_scope_ip, metavar='')
    parser.add_argument('-tm', '--target_mac',
        help='MAC address of target on network [Self / valid MAC address] (default: Random)',
        type=check_arg_mac, metavar='')
    parser.add_argument('-sm', '--source_mac',
        help='MAC address of source on network [Self / valid MAC address] (default: Random)',
        type=check_arg_mac, metavar='')
    parser.add_argument('-t_p', '--target_port',
        help='Port of target on network (default: Random)', type=check_arg_port, metavar='')
    parser.add_argument('-s_p', '--source_port',
        help='Port of source on network (default: Random)', type=check_arg_port, metavar='')
    parser.add_argument('-ip', '--int_protocol',
        help='Specify the internet protocol [IPv4 / IPv6] (default: Random)',
        type=check_arg_iprotocol, metavar='')
    parser.add_argument('-tp', '--trans_protocol',
        help='Specify the transport protocol [TCP / UDP] (default: Random)',
        type=check_arg_tprotocol, metavar='')
    parser.add_argument('-c', '--cast',
        help='Specify cast types [unicast / multicast / broadcast] (default: Random)',
        type=check_arg_cast, metavar='')
    parser.add_argument('-hd', '--headers',
        help='Disable randomised headers (default: Random)', action='store_false')
    parser.add_argument('-vl', '--vlan', help='adds vlan tag', action='store_true')
    parser.add_argument('-min', '--min_length',
        help='Specify minimum packet length (default: Ethertype minimum)',
        type=check_arg_packet_length_int, metavar='')
    parser.add_argument('-max', '--max_length',
        help='Specify maximum packet length (default: Ethertype maximum)',
        type=check_arg_packet_length_int, metavar='')
    parser.add_argument('-s', '--seed',
        help='Specify seed to generate packets (default: Random seed)',
        type=check_arg_positive_int, metavar='')

    return parser.parse_args(args)


def check_arg_specific_ip(string: str) -> str:
    """ Argument check method for specific IP form

    Parameters:
        string (str): String to check if in correct form

    Returns:
        string (str): Valid string in correct form
    """
    if len(string) > 17 or len(string) < 7 or not isinstance(string, str) or \
            not re.search(REGEX_SPECIFIC_IP, string):
        raise argparse.ArgumentTypeError(
            'Not a valid IP address. Required to be in standard format X.X.X.X'
        )
    return string


def check_arg_scope_ip(string: str) -> str:
    """ Argument check method for scope IP form

    Parameters:
        string (str): String to check if in correct form

    Returns:
        string (str): Valid string in correct form
    """
    if len(string) > 17 or len(string) < 7 or not isinstance(string, str) or \
            not re.search(REGEX_SCOPE_IP, string):
        raise argparse.ArgumentTypeError(
            'Not a valid IP address. Required to be in standard format X.X.X.X'
        )
    return string


def check_arg_name(string: str) -> str:
    """ Argument check method for interface name

    Parameters:
        string (str): String to check if in correct form

    Returns:
        string (str): Valid string in correct form
    """
    if len(string) > 31 or len(string) < 1 or not isinstance(string, str):
        raise argparse.ArgumentTypeError(
            'Name is required to be between 0 and 32 characters.'
        )
    return string


def check_arg_mac(string: str) -> str:
    """ Argument check method for mac address form

    Parameters:
        string (str): String to check if in correct form

    Returns:
        string (str): Valid string in correct form
    """
    if string.lower() == 'self':
        return string.lower()

    if len(string) > 17 or len(string) < 12 or not isinstance(string, str) or \
            not re.search(REGEX_MAC, string):
        raise argparse.ArgumentTypeError(
            'Not a valid MAC address. Required to be in a standard format '\
            'X:X:X:X:X:X or X-X-X-X-X-X or X.X.X'
        )
    return string


def check_arg_iprotocol(string: str) -> int:
    """ Argument check method for internet protocol options, converts to hex value

    Parameters:
        string (str): String to check if is a valid option

    Returns:
        value (int): Valid sex value of internet protocol
    """
    if len(string) > 5 or not isinstance(string, str) or \
            string.lower() not in INTERNET_PROTOCOLS:
        raise argparse.ArgumentTypeError(
            'Not a supported internet protocol input. Required to be IPv4, IPv6 or Jumbo'
        )
    return INTERNET_PROTOCOLS_INFO[string.lower()]['value']


def check_arg_tprotocol(string: str) -> int:
    """ Argument check method for transport protocol options, converts to hex value

    Parameters:
        string (str): String to check if is a valid option

    Returns:
        value (int): Valid hex value of transport protocol
    """
    if len(string) > 3 or not isinstance(string, str) or \
            string.lower() not in TRANSPORT_PROTOCOLS:
        raise argparse.ArgumentTypeError(
            'Not a supported transport protocol input. Required to be either UDP or TCP'
        )
    return TRANSPORT_PROTOCOLS_INFO[string.lower()]['value']


def check_arg_port(string: str) -> int:
    """ Argument check method for port number

    Parameters:
        string (str): String to check if is a valid option

    Returns:
        value (int): Valid Port number
    """
    try:
        value = int(string)
    except Exception as exception:
        raise argparse.ArgumentTypeError(
            'You must enter an integer for the port input.'
        ) from exception
    else:
        if value < 1 or value > MAX_PORT:
            raise argparse.ArgumentTypeError(
                'You must enter an integer between 0 and 65535 for the port input.'
            )
    return value


def check_arg_cast(string: str) -> str:
    """ Argument check method for cast type option

    Parameters:
        string (str): String to check if is a valid option

    Returns:
        str (str): Valid cast type option
    """
    if not isinstance(string, str) or string.lower() not in CAST_TYPES:
        raise argparse.ArgumentTypeError(
            'Not a supported cast type input. Required to be either unicast, multicast or broadcast'
        )
    return string.lower()


def check_arg_positive_int(string: str) -> int:
    """ Argument check method for argument to be a positive integer

    Parameters:
        string (str): String to check if is a valid option

    Returns:
        value (int): A valid positive integer
    """
    try:
        value = int(string)
    except Exception as exception:
        raise argparse.ArgumentTypeError(
            'You must enter an integer.'
        ) from exception
    else:
        if value <= 0:
            raise argparse.ArgumentTypeError(
                'You must enter a positive integer.'
            )
    return value


def check_arg_packet_length_int(string):
    """ Argument check method for packet length (Must be between 48 and 9000)

    Parameters:
        string (str): String to check if is a valid option

    Returns:
        value (int): A valid packet length
    """
    try:
        value = int(string)
    except Exception as exception:
        raise argparse.ArgumentTypeError(
            'You must enter an integer.'
        ) from exception
    else:
        if value < 48 or value > 9000:
            raise argparse.ArgumentTypeError(
                'You must enter a positive integer between 48 and 9000'
            )
    return value


class Args():
    """ Argument Class to store run arguments"""

    def __init__(self, args: dict):
        """ Args class built-in initialiser"""
        self.target_ip = None
        self.network_interface = None
        self.n_packets = None
        self.source_ip = None
        self.target_mac = None
        self.source_mac = None
        self.target_port = None
        self.source_port = None
        self.int_protocol = None
        self.trans_protocol = None
        self.cast = None
        self.headers = None
        self.vlan = None
        self.min_length = None
        self.max_length = None
        self.seed = None

        for key, value in args.items():
            if key in self.__dict__:
                setattr(self, key, value)

    def _dict(self) -> dict:
        """ Method to output class attributes as a dictionary"""
        return self.__dict__

    def __str__(self) -> str:
        """Built-in str method"""
        return f"[{', '.join(f'{key}: {val}' for key, val in self.__dict__.items())}]"

    def __repr__(self) -> str:
        """Built-in repr method"""
        return f"Object: {self.__class__.__name__} [{', '.join(list(self.__dict__.values()))}]"
