# Python library imports
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict, List
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


def valid_specific_IP(string: str, min: int=7, max: int= 17) -> str:
    """ Validation test for a specific IP address

    Parameters:
    string (str): IP address
    min (int): Minimum length of IP address
    max (int): Maximum length of IP address

    Returns:
    str: Valid IP address
    """
    if string is None:
        return string

    if type(string) is not str:
        raise ex.IpAddressInvalidTypeError(
            f'Not a valid IP address type. Received: {string} ({type(string)})'
            f'Required to be in standard format X.X.X.X'
        )
    if len(string) > max:
        raise ex.IpAddressTooLongValueError(
            f'Not a valid IP address, cannot be longer than {max} characters.'
            f'(Length={len(string)}) Required to be in standard format X.X.X.X'
        )
    if len(string) < min:
        raise ex.IpAddressTooShortValueError(
            f'Not a valid IP address, cannot be shorter than {min} characters.'
            f'(Length={len(string)}) Required to be in standard format X.X.X.X'
        )
    if not re.search(REGEX_SPECIFIC_IP, string):
        raise ex.IpAddressInvalidFormatError(
            f'Not a valid IP address. ({string})'
            f'Required to be in standard format X.X.X.X'
        )
    return string.upper()


def valid_scope_IP(string: str, min: int=7, max: int= 17) -> str:
    """ Validation test for a scope IP address

    Parameters:
    string (str): IP address
    min (int): Minimum length of IP address
    max (int): Maximum length of IP address

    Returns:
    str: Valid IP address
    """
    if string is None:
        return string

    if type(string) is not str:
        raise ex.IpAddressInvalidTypeError(
            f'Not a valid IP address type. Received: {string} ({type(string)})'
            f'Required to be in standard format X.X.X.X'
        )
    if len(string) > max:
        raise ex.IpAddressTooLongValueError(
            f'Not a valid IP address, cannot be longer than {max} characters.'
            f'(Length={len(string)}) Required to be in standard format X.X.X.X'
        )
    if len(string) < min:
        raise ex.IpAddressTooShortValueError(
            f'Not a valid IP address, cannot be shorter than {min} characters.'
            f'(Length={len(string)}) Required to be in standard format X.X.X.X'
        )
    if not re.search(REGEX_SCOPE_IP, string):
        raise ex.IpScopeAddressInvalidFormatError(
            f'Not a valid IP address. ({string})'
            f'Required to be in standard format X.X.X.X'
        )
    return string.upper()


def valid_mac(string: str, min: int=12, max: int= 17) -> str:
    """ Validation test for a MAC address

    Parameters:
    string (str): MAC address
    min (int): Minimum length of MAC address
    max (int): Maximum length of MAC address

    Returns:
    str: Valid MAC address
    """
    if string is None:
        return string

    if type(string) is not str:
        raise ex.MacAddressInvalidTypeError(
            f'Not a valid MAC address type. Received: {string} ({type(string)})'
            f'Required to be in a standard format X:X:X:X:X:X or X-X-X-X-X-X or X.X.X'
        )
    if len(string) > max:
        raise ex.MacAddressTooLongValueError(
            f'Not a valid MAC address, cannot be longer than {max} characters. (Length={len(string)})'
            f'Required to be in a standard format X:X:X:X:X:X or X-X-X-X-X-X or X.X.X'
        )
    if len(string) < min:
        raise ex.MacAddressTooShortValueError(
            f'Not a valid MAC address, cannot be shorter than {min} characters. (Length={len(string)})'
            f'Required to be in a standard format X:X:X:X:X:X or X-X-X-X-X-X or X.X.X'
        )
    if not re.search(REGEX_MAC, string):
        raise ex.MacAddressInvalidFormatError(
            f'Not a valid MAC address. ({string})'
            f'Required to be in a standard format X:X:X:X:X:X or X-X-X-X-X-X or X.X.X'
        )
    return string.upper()


def valid_port(value: Any, min: int=1, max: int= MAX_PORT) -> int:
    """ Validation test for a Port number

    Parameters:
    value (Any): Port number as a convertable datatype (str/int/float)
    min (int): Minimum port number
    max (int): Maximum port number

    Returns:
    str: Valid MAC address
    """
    if value is None:
        return value

    if type(value) not in [str, float, int]:
        raise ex.PortInvalidTypeError(
            f'Not a valid port number type. Received: {value} ({type(value)})'
        )
    try:
        value = int(value)
    except ValueError as e:
        raise ex.PortInvalidFormatError(
            f'Not a valid port number format. Received: {value}'
        )
    if value < min or value > max:
        raise ex.PortInvalidValueError(
            f'Not a valid port number value. (Value={value})'
            f'It must be an integer between {min} and {max}'
        )
    return value


def valid_name(string: Any, min: int=1, max: int=31) -> int:
    """ Validation test for a name

    Parameters:
    string (str): Name as a string
    min (int): Minimum string length
    max (int): Maximum string length

    Returns:
    str: Valid string
    """
    if string is None:
        return string

    if type(string) is not str:
        raise ex.NameInvalidTypeError(
            f'Not a valid name type. Received: {string} ({type(string)})'
        )
    if len(string) > max:
        raise ex.NameTooLongError(
            f'Not a valid name, cannot be longer than {max} characters. (Length={len(string)})'
        )
    if len(string) < min:
        raise ex.NameTooShortError(
            f'Not a valid name, cannot be shorter than {min} characters. (Length={len(string)})'
        )
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
            f'Must be Host class objects. Received: {host} type({type(host)}'
        )
    if host.ip is None:
        raise ex.HostNoIpAddressError(
            f'Host IP instance attribute cannot be None.'
        )
    if host.mac is None:
        raise ex.HostNoMacAddressError(
            f'Host MAC instance attribute cannot be None.'
        )
    if host.port is None:
        raise ex.HostNoPortAddressError(
            f'Host port instance attribute cannot be None.'
        )
    return host


def valid_packet_info(info: Dict) -> Dict:
    """ Validation test for valid packet info

    Parameters:
    info (Dict): Info dictionary contain key,value pairs

    Returns:
    dict: Valid packet info dictionary object
    """
    must_contain = ['int_protocol', 'trans_protocol', 'cast', 'length', 'vlan', 'headers']

    if type(info) is not dict:
        raise ex.PacketInfoTypeError(
            f'Not a valid packet info data type. Received: {info} ({type(info)})'
            f'Required to be a dict with at least the following keys: {must_contain}'
        )

    info_keys_set = set(info.keys())
    for key in must_contain:
        if key not in info_keys_set:
            raise ex.PacketInfoKeysError(
            f'Packet info does not have the correct minimal entries. '
            f'Received: {info_keys_set}, Requires: {must_contain}'
        )
    
    if info['headers']:
        must_contain.append('ip_header')
        if int(info['trans_protocol']) == int(TRANSPORT_PROTOCOLS_INFO['tcp']['value']):
            must_contain.append('tcp_header')

    if len(must_contain) != len(info):
        raise ex.PacketInfoLengthError(
            f'{must_contain}'
            f'Packet info received unexpected number of values, {len(info)}. Expected {len(must_contain)}'
        )
    must_contain_set = set(must_contain)
    if must_contain_set != info_keys_set:
        if must_contain_set - info_keys_set:
            raise ex.PacketInfoMissingEntriesError(
                f'Packet info has missing values: {must_contain_set - info_keys_set}'
            )
        if info_keys_set - must_contain_set:
            raise ex.PacketInfoExtraEntriesError(
                f'Packet info has incorrect values: {info_keys_set - must_contain_set}'
            )
    return info


def valid_seed(value: int, min: int=0, max: int=sys.maxsize) -> int:
    """ Validation test for valid seed

    Parameters:
    value (Any): Seed value as a convertable datatype (str/int/float)
    min (int): Minimum Seed value
    max (int): Maximum Seed value

    Returns:
    int: Valid Seed value
    """
    if value is None:
        return value

    if type(value) not in [str, float, int]:
        raise ex.SeedInvalidTypeError(
            f'Not a valid Seed type. Received: {value} ({type(value)})'
        )
    try:
        value = int(value)
    except ValueError as e:
        raise ex.SeedInvalidFormatError(
            f'Not a valid Seed format. Received: {value}'
        )
    if value < min or value > max:
        raise ex.SeedInvalidValueError(
            f'Not a valid Seed value. (Value={value})'
            f'It must be an integer between {min} and {max}'
        )
    return value
