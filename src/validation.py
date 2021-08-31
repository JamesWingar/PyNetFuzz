"""
Contains validation methods for parsing values
"""
# Python library imports
from __future__ import annotations
from typing import TYPE_CHECKING, Union
import re
import sys
# Package imports
import src.exceptions as ex
from src.const import (
    REGEX_SPECIFIC_IP,
    REGEX_SCOPE_IP,
    REGEX_MAC,
    MAX_PORT,
    TRANSPORT_PROTOCOLS_INFO,
)

if TYPE_CHECKING:
    from src.hosts import Host
    from src.packet import PacketDetails


def valid_specific_ip(string: str, minimum: int=7, maximum: int= 17) -> str:
    """ Validation test for a specific IP address

    Parameters:
        string (str): IP address
        minimum (int): Minimum length of IP address
        maximum (int): Maximum length of IP address

    Returns:
        str: Valid IP address
    """
    if string is None:
        return string

    if not isinstance(string, str):
        raise ex.IpAddressInvalidTypeError(
            f'Not a valid IP address type. Received: {string} ({type(string)}) '
            f'Required to be in standard format X.X.X.X')
    if len(string) > maximum:
        raise ex.IpAddressTooLongValueError(
            f'Not a valid IP address, cannot be longer than {maximum} chars '
            f'(len={len(string)}) Required to be in standard format X.X.X.X')
    if len(string) < minimum:
        raise ex.IpAddressTooShortValueError(
            f'Not a valid IP address, cannot be shorter than {minimum} chars '
            f'(len={len(string)}) Required to be in standard format X.X.X.X')
    if not re.search(REGEX_SPECIFIC_IP, string):
        raise ex.IpAddressInvalidFormatError(
            f'Not a valid IP address. ("{string}") '
            f'Required to be in standard format X.X.X.X')
    return string.upper()


def valid_scope_ip(string: str, minimum: int=7, maximum: int= 17) -> str:
    """ Validation test for a scope IP address

    Parameters:
        string (str): IP address
        minimum (int): Minimum length of IP address
        maximum (int): Maximum length of IP address

    Returns:
        str: Valid IP address
    """
    if string is None:
        return string

    if not isinstance(string, str):
        raise ex.IpAddressInvalidTypeError(
            f'Not a valid IP address type. Received: {string} ({type(string)})'
            f'Required to be in standard format X.X.X.X'
        )
    if len(string) > maximum:
        raise ex.IpAddressTooLongValueError(
            f'Not a valid IP address, cannot be longer than {maximum} chars '
            f'(len={len(string)}) Required to be in standard format X.X.X.X')
    if len(string) < minimum:
        raise ex.IpAddressTooShortValueError(
            f'Not a valid IP address, cannot be shorter than {minimum} chars '
            f'(len={len(string)}) Required to be in standard format X.X.X.X')
    if not re.search(REGEX_SCOPE_IP, string):
        raise ex.IpScopeAddressInvalidFormatError(
            f'Not a valid IP address. ("{string}") '
            f'Required to be in standard format X.X.X.X')
    return string.upper()


def valid_mac(string: str, minimum: int=12, maximum: int= 17) -> str:
    """ Validation test for a MAC address

    Parameters:
        string (str): MAC address
        minimum (int): Minimum length of MAC address
        maximum (int): Maximum length of MAC address

    Returns:
        str: Valid MAC address
    """
    if string is None:
        return string

    if not isinstance(string, str):
        raise ex.MacAddressInvalidTypeError(
            f'Not a valid MAC address type. Received: {string} ({type(string)}) '
            f'Required to be in a standard format X:X:X:X:X:X or X-X-X-X-X-X or X.X.X')
    if len(string) > maximum:
        raise ex.MacAddressTooLongValueError(
            f'Not a valid MAC address, cannot be longer than {maximum} chars (len={len(string)}) '
            f'Required to be in a standard format X:X:X:X:X:X or X-X-X-X-X-X or X.X.X')
    if len(string) < minimum:
        raise ex.MacAddressTooShortValueError(
            f'Not a valid MAC address, cannot be shorter than {minimum} chars (len={len(string)}) '
            f'Required to be in a standard format X:X:X:X:X:X or X-X-X-X-X-X or X.X.X')
    if not re.search(REGEX_MAC, string):
        raise ex.MacAddressInvalidFormatError(
            f'Not a valid MAC address. ("{string}") '
            f'Required to be in a standard format X:X:X:X:X:X or X-X-X-X-X-X or X.X.X')
    return string.upper()


def valid_port(value: Union[str, int, float], minimum: int=1, maximum: int= MAX_PORT) -> int:
    """ Validation test for a Port number

    Parameters:
        value (str|int|float): Port number as a convertable datatype
        minimum (int): Minimum port number
        maximum (int): Maximum port number

    Returns:
        str: Valid MAC address
    """
    if value is None:
        return value

    if not isinstance(value, (str, float, int)):
        raise ex.PortInvalidTypeError(
            f'Not a valid port number type. Received: {value} ({type(value)})')
    try:
        value = int(value)
    except ValueError as exception:
        raise ex.PortInvalidFormatError(
            f'Not a valid port number format. Received: {value}') from exception
    if value < minimum or value > maximum:
        raise ex.PortInvalidValueError(
            f'Not a valid port number value. (Value={value}) '
            f'It must be an integer between {minimum} and {maximum}')
    return value


def valid_name(string: str, minimum: int=1, maximum: int=31) -> int:
    """ Validation test for a name

    Parameters:
        string (str): Name as a string
        minimum (int): Minimum string length
        maximum (int): Maximum string length

    Returns:
        str: Valid string
    """
    if string is None:
        return string

    if not isinstance(string, str):
        raise ex.NameInvalidTypeError(
            f'Not a valid name type. Received: {string} ({type(string)})')
    if len(string) > maximum:
        raise ex.NameTooLongError(
            f'Not a valid name, cannot be longer than {maximum} chars (len={len(string)})')
    if len(string) < minimum:
        raise ex.NameTooShortError(
            f'Not a valid name, cannot be shorter than {minimum} chars (len={len(string)})')
    return string


def valid_host(host: Host) -> Host:
    """ Validation test for valid Host class

    Parameters:
        host (Host): Host class object

    Returns:
        Host: Valid Host object
    """
    from src.hosts import Host
    if not isinstance(host, Host):
        raise ex.InvalidHostError(
            f'Must be Host class objects. Received: {host} type({type(host)}')
    if host.ip_addr is None:
        raise ex.HostNoIpAddressError(
            'Host IP instance attribute cannot be None.')
    if host.mac is None:
        raise ex.HostNoMacAddressError(
            'Host MAC instance attribute cannot be None.')
    if host.port is None:
        raise ex.HostNoPortAddressError(
            'Host port instance attribute cannot be None.')
    return host


def valid_packet_details(details: PacketDetails, must_contain: list=None) -> PacketDetails:
    """ Validation test for valid intial (before randomising) packet details

    Parameters:
        details (PacketDetails): PacketDetails object containing initial packet
            details as attributes before being randomised

    Returns:
        PacketDetails: Valid PacketDetails object
    """
    from src.packet import PacketDetails
    if not must_contain:
        must_contain = ['int_protocol', 'trans_protocol', 'cast',
                        'vlan', 'headers', 'min_length', 'max_length']

    if not isinstance(details, PacketDetails):
        raise ex.InvalidPacketDetailsError(
            f'Not a valid instace of PacketDetails. Received: {details} type({type(details)})')

    for key in must_contain:
        if not hasattr(details, key):
            raise ex.PacketDetailsAttributeError(
            f'Packet details does not have the correct minimal entries. '
            f'Missing: {key}, Requires: {must_contain}')
    return details


def valid_complete_packet_details(details: PacketDetails) -> PacketDetails:
    """ Validation test for a valid complete packet details (All requirements for a Packet)

    Parameters:
        details (PacketDetails): A complete PacketDetails object containing all
            required details to create a packet as attributes

    Returns:
        PacketDetails: Valid PacketDetails object
    """
    must_contain = ['int_protocol', 'trans_protocol', 'cast', 'vlan', 'headers', 'length']
    details = valid_packet_details(details, must_contain)

    if details.get('headers', None):
        must_contain.append('ip_header')
        if int(details.get('trans_protocol')) == int(TRANSPORT_PROTOCOLS_INFO['tcp']['value']):
            must_contain.append('tcp_header')

    must_contain_set = set(must_contain)
    details_attr_set = set()
    for key in must_contain:
        if hasattr(details, key):
            details_attr_set.add(key)

    if must_contain_set != details_attr_set:
        if must_contain_set - details_attr_set:
            raise ex.PacketDetailsMissingEntriesError(
                f'Packet details has missing values: {must_contain_set - details_attr_set}')
    return details


def valid_packet_info(info: dict) -> dict:
    """ Validation test for valid packet info

    Parameters:
    info (dict): dictionary containing required key,value pairs

    Returns:
    dict: Valid packet info dictionary object
    """
    must_contain = ['int_protocol', 'trans_protocol', 'cast', 'vlan', \
                    'headers', 'min_length', 'max_length']

    if not isinstance(info, dict):
        raise ex.PacketInfoTypeError(
            f'Not a valid packet info data type. Received: {info} ({type(info)}) '
            f'Required to be a dict with at least the following keys: {must_contain}')

    info_keys_set = set(info.keys())
    must_contain_set = set(must_contain)
    if must_contain_set != info_keys_set:
        if must_contain_set - info_keys_set:
            raise ex.PacketInfoMissingEntriesError(
                f'Packet info has missing values: {must_contain_set - info_keys_set}')
        if info_keys_set - must_contain_set:
            raise ex.PacketInfoExtraEntriesError(
                f'Packet info has incorrect values: {info_keys_set - must_contain_set}')
    return info


def valid_seed(value: Union[str, int, float], minimum: int=0, maximum: int=sys.maxsize) -> int:
    """ Validation test for valid seed

    Parameters:
    value (str|int|float): Seed value as a convertable datatype
    minimum (int): Minimum Seed value
    maximum (int): Maximum Seed value

    Returns:
    int: Valid Seed value
    """
    if value is None:
        return value

    if not isinstance(value, (str, float, int)):
        raise ex.SeedInvalidTypeError(
            f'Not a valid Seed type. Received: {value} ({type(value)})')
    try:
        value = int(value)
    except ValueError as exception:
        raise ex.SeedInvalidFormatError(
            f'Not a valid Seed format. Received: {value}') from exception
    if value < minimum or value > maximum:
        raise ex.SeedInvalidValueError(
            f'Not a valid Seed value. (Value={value}) '
            f'It must be an integer between {minimum} and {maximum}')
    return value


def valid_number(value: Union[str, int, float], minimum: int=0, maximum: int=sys.maxsize) -> int:
    """ Validation test for valid seed

    Parameters:
    value (str|int|float): value as a convertable datatype
    minimum (int): Minimum Seed value
    max (int): Maximum Seed value

    Returns:
    int: Valid Seed value
    """
    if value is None:
        return value

    if not isinstance(value, (str, float, int)):
        raise ex.IntegerInvalidTypeError(
            f'Not a valid number type. Received: {value} ({type(value)})')
    try:
        value = int(value)
    except ValueError as exception:
        raise ex.IntegerInvalidFormatError(
            f'Not a valid number format. Received: {value}') from exception
    if value < minimum:
        raise ex.IntegerTooSmallError(
            f'Number value too small, not a valid value (Value={value}) '
            f'It must be an integer between {minimum} and {maximum}')
    if value > maximum:
        raise ex.IntegerTooLargeError(
            f'Number value too large, not a valid value (Value={value}) '
            f'It must be an integer between {minimum} and {maximum}')
    return value
