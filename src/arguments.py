import argparse
import re
from src import const


# regular expression for validating an IP address
REGEX_IP = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
# regular expression for validating a MAC address
REGEX_MAC = "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})|([0-9a-fA-F]{4}\\.[0-9a-fA-F]{4}\\.[0-9a-fA-F]{4})$"

import sys

def parse_args(args=None):
    """Build and parse command line positional and optional arguments and returns as a Namespace.

    Returns:
        Class: Argparse namespace class with command line arguments.
    """

    parser = argparse.ArgumentParser(
        prog='Network Fuzzing',
        usage='\n[Filename] %(prog)s \n\
[Positional arguments] <target IP> <Network interface> <N packets> \n\
[Optional arguments] [source_ip | target_mac | source_mac | target_port | source_port | int_protocol | trans_protocol | cast | headers | vlan | min_packet | max_packet | seed]',
        description='Creates and sends suedo-random network packets as part of a Fuzz Test.',
        epilog='For more detail go to the ReadMe file in main directory.')
    
    # Positional arguments
    parser.add_argument(
        'target_ip', help='IP address of target on network', type=validate_IP)
    parser.add_argument(
        'network_interface', help='Name of the interface connected to the local network', type=validate_name)
    parser.add_argument(
        'n_packets', help='Number of packets to be sent', type=validate_positive_int)
    
    # Optional arguments
    parser.add_argument(
        '-sip', '--source_ip', help='IP address of source on network (default: Random)', type=validate_IP, metavar='')
    parser.add_argument(
        '-tm', '--target_mac', help='MAC address of target on network [Self / valid MAC address] (default: Random)', type=validate_MAC, metavar='')
    parser.add_argument(
        '-sm', '--source_mac', help='MAC address of source on network [Self / valid MAC address] (default: Random)', type=validate_MAC, metavar='')
    parser.add_argument(
        '-t_p', '--target_port', help='Port of target on network (default: Random)', type=validate_port, metavar='')
    parser.add_argument(
        '-s_p', '--source_port', help='Port of source on network (default: Random)', type=validate_port, metavar='')
    parser.add_argument(
        '-ip', '--int_protocol', help='Specify the internet protocol [IPv4 / IPv6] (default: Random)', type=validate_iprotocol, metavar='')
    parser.add_argument(
        '-tp', '--trans_protocol', help='Specify the transport protocol [TCP / UDP] (default: Random)', type=validate_tprotocol, metavar='')
    parser.add_argument(
        '-c', '--cast', help='Specify cast types [unicast / multicast / broadcast] (default: Random)', type=validate_cast, metavar='')
    parser.add_argument(
        '-hd', '--headers', help='Disable randomised headers (default: Random)', action='store_false')
    parser.add_argument(
        '-vl', '--vlan', help='adds vlan tag', action='store_true')
    parser.add_argument(
        '-min', '--min_packet', help='Specify minimum packet length (default: Ethertype minimum)', type=validate_packet_length_int, metavar='')
    parser.add_argument(
        '-max', '--max_packet', help='Specify maximum packet length (default: Ethertype maximum)', type=validate_packet_length_int, metavar='')
    parser.add_argument(
        '-s', '--seed', help='Specify seed to generate packets (default: Random seed)', type=validate_positive_int, metavar='')

    return vars(parser.parse_args(args))


def validate_IP(string):
    if len(string) > 17 or len(string) < 7 or type(string) != str or not re.search(REGEX_IP, string):
        raise argparse.ArgumentTypeError(
            'Not a valid IP address. Required to be in standard format X.X.X.X'
        )
    return string


def validate_name(string):
    if len(string) > 31 or len(string) < 1 or type(string) != str:
        raise argparse.ArgumentTypeError(
            'Name is required to be between 0 and 32 characters.'
        )
    return string


def validate_MAC(string):
    if string.lower() == 'self':
        return string.lower()

    if len(string) > 17 or len(string) < 12 or type(string) != str or not re.search(REGEX_MAC, string):
        raise argparse.ArgumentTypeError(
            'Not a valid MAC address. Required to be in a standard format X:X:X:X:X:X or X-X-X-X-X-X or X.X.X'
        )
    return string


def validate_iprotocol(string):
    if len(string) > 5 or type(string) != str or string.lower() not in const.INTERNET_PROTOCOLS:
        raise argparse.ArgumentTypeError(
            'Not a supported internet protocol input. Required to be IPv4, IPv6 or Jumbo'
        )
    return const.INTERNET_PROTOCOLS_INFO[string.lower()]['value']


def validate_tprotocol(string):
    if len(string) > 3 or type(string) != str or string.lower() not in const.TRANSPORT_PROTOCOLS:
        raise argparse.ArgumentTypeError(
            'Not a supported transport protocol input. Required to be either UDP or TCP'
        )
    return const.TRANSPORT_PROTOCOLS_INFO[string.lower()]['value']


def validate_port(string):
    try:
        value = int(string)
    except:
        raise argparse.ArgumentTypeError(
            'You must enter an integer for the port input. Required to be between 0 and 65535'
        )
    else:
        if value < 1 or value > const.MAX_PORT:
            raise argparse.ArgumentTypeError(
                'You must enter an integer for the port input. Required to be between 0 and 65535'
            )
    return value


def validate_cast(string):
    if type(string) != str or string.lower() not in const.CAST_TYPES:
        raise argparse.ArgumentTypeError(
            'Not a supported cast type input. Required to be either unicast, multicast or broadcast'
        )
    return string.lower()


def validate_positive_int(string):
    try:
        value = int(string)
    except:
        raise argparse.ArgumentTypeError(
            'You must enter a positive integer.'
        )
    else:
        if value <= 0:
            raise argparse.ArgumentTypeError(
                'You must enter a positive integer.'
            )
    return value


def validate_packet_length_int(string):
    try:
        value = int(string)
    except:
        raise argparse.ArgumentTypeError(
            'You must enter a positive integer between 48 and 9000'
        )
    else:
        if value < 48 or value > 9000:
            raise argparse.ArgumentTypeError(
                'You must enter a positive integer between 48 and 9000'
            )
    return value
