import re
from typing import Any

import src.exceptions as ex
from src.const import (
    REGEX_SPECIFIC_IP,
    REGEX_SCOPE_IP,
    REGEX_MAC,
    MAX_PORT,
)


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
    if type(string) is not str:
        raise ex.IpAddressInvalidValueError(
            f'Not a valid IP address. ({string})'
            f'Required to be in standard format X.X.X.X'
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
    if type(string) is not str:
        raise ex.IpAddressInvalidValueError(
            f'Not a valid IP address. ({string})'
            f'Required to be in standard format X.X.X.X'
        )
    if not re.search(REGEX_SCOPE_IP, string):
        raise ex.IpAddressInvalidFormatError(
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
    if type(string) is not str:
        raise ex.MacAddressInvalidValueError(
            f'Not a valid MAC address. ({string})'
            f'Required to be in a standard format X:X:X:X:X:X or X-X-X-X-X-X or X.X.X'
        )
    if not re.search(REGEX_MAC, string):
        raise ex.MacAddressInvalidFormatError(
            f'Not a valid MAC address. ({string})'
            f'Required to be in a standard format X:X:X:X:X:X or X-X-X-X-X-X or X.X.X'
        )
    return string.upper()


def valid_port(string: Any, min: int=1, max: int= MAX_PORT) -> int:
    """ Validation test for a Port number

    Parameters:
    string (Any): Port number as a convertable datatype (str/int/float)
    min (int): Minimum port number
    max (int): Maximum port number
    Returns:
    str: Valid MAC address
    """
    if string is None:
        return string

    try:
        value = int(string)
    except:
        raise ex.PortInvalidFormatError(
            f'Not a valid port number format. (Input={string})'
            f'It must be an integer between {min} and {max}'
        )
    else:
        if value < min or value > max:
            raise ex.PortInvalidValueError(
                f'Not a valid port number value. (Value={value})'
                f'It must be an integer between {min} and {max}'
            )
    return string


def valid_name(string: Any, min: int=1, max: int= 31) -> int:
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

    if len(string) > max:
        raise ex.NameTooLongError(
            f'Not a valid name, cannot be longer than {max} characters. (Length={len(string)})'
        )
    if len(string) < min:
        raise ex.NameTooShortError(
            f'Not a valid name, cannot be shorter than {min} characters. (Length={len(string)})'
        )
    if type(string) is not str:
        raise ex.NameInvalidFormatError(
            f'Not a valid name. ({string})'
        )
    return string.upper()
