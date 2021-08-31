"""
Contains all module exception classes
"""
#--- BASE EXCEPTIONS----
# Base Validation Class
class BaseValidationError(ValueError):
    """Base validation error"""

#--- CLASS EXCEPTIONS----
class InvalidHostError(BaseValidationError):
    """Raised when host is invalid"""

class InvalidPacketError(BaseValidationError):
    """Raised when packet is invalid"""

class InvalidPacketDetailsError(BaseValidationError):
    """Raised when packet details are invalid"""

class InvalidRandomiserError(BaseValidationError):
    """Raised when randomiser is invalid"""

#--- HOST EXCEPTIONS----
class HostNoIpAddressError(BaseValidationError):
    """Raised when IP address is missing"""

class HostNoMacAddressError(BaseValidationError):
    """Raised when MAC address is missing"""

class HostNoPortAddressError(BaseValidationError):
    """Raised when Port is missing"""

class HostGetLocalIpError(BaseValidationError):
    """Raised when failed to get local IP"""

class HostGetLocalMacError(BaseValidationError):
    """Raised when failed to get local MAC"""

class HostGetRemoteMacError(BaseValidationError):
    """Raised when failed to get remote MAC"""

#--- PACKET EXCEPTIONS----

#--- PACKET INFO EXCEPTIONS----
class PacketInfoTypeError(BaseValidationError):
    """Raised when packet info is the wrong type"""

class PacketInfoMissingEntriesError(BaseValidationError):
    """Raised when packet info is missing entries"""

class PacketInfoExtraEntriesError(BaseValidationError):
    """Raised when packet info has additional entries"""

#--- PACKET DETAILS EXCEPTIONS----
class PacketDetailsTypeError(BaseValidationError):
    """Raised when packet details is the wrong type"""

class PacketDetailsAttributeError(BaseValidationError):
    """Raised when packet details has the wrong attribute"""

class PacketDetailsMissingEntriesError(BaseValidationError):
    """Raised when packet details is missing entries"""

#--- RANDOMISER EXCEPTIONS----

#--- VALIDATION EXCEPTIONS----
# IP address
class IpAddressInvalidTypeError(BaseValidationError):
    """Raised when IP address is wrong type"""

class IpAddressInvalidFormatError(BaseValidationError):
    """Raised when IP address is wrong format"""

class IpScopeAddressInvalidFormatError(BaseValidationError):
    """Raised when Scope IP address is wrong format"""

class IpAddressInvalidValueError(BaseValidationError):
    """Raised when IP address is wrong value"""

class IpScopeAddressInvalidValueError(BaseValidationError):
    """Raised when Scope IP address is wrong value"""

class IpAddressTooLongValueError(BaseValidationError):
    """Raised when IP address is too long"""

class IpAddressTooShortValueError(BaseValidationError):
    """Raised when IP address is too short"""

# Mac address
class MacAddressInvalidTypeError(BaseValidationError):
    """Raised when MAC address is wrong type"""

class MacAddressInvalidFormatError(BaseValidationError):
    """Raised when MAC address is wrong format"""

class MacAddressInvalidValueError(BaseValidationError):
    """Raised when MAC address is wrong value"""

class MacAddressTooLongValueError(BaseValidationError):
    """Raised when MAC address is too long"""

class MacAddressTooShortValueError(BaseValidationError):
    """Raised when MAC address is too short"""

# Port
class PortInvalidTypeError(BaseValidationError):
    """Raised when Port is wrong type"""

class PortInvalidFormatError(BaseValidationError):
    """Raised when Port is wrong format"""

class PortInvalidValueError(BaseValidationError):
    """Raised when Port is wrong value"""

# Name
class NameInvalidTypeError(BaseValidationError):
    """Raised when name string is wrong type"""

class NameInvalidFormatError(BaseValidationError):
    """Raised when name string is wrong format"""

class NameInvalidValueError(BaseValidationError):
    """Raised when name string is wrong value"""

class NameTooLongError(BaseValidationError):
    """Raised when name string is too long"""

class NameTooShortError(BaseValidationError):
    """Raised when name string is too short"""

# Internet protocol
class InternetProtocolInvalidFormatError(BaseValidationError):
    """Raised when internet protocol is wrong format"""

class InternetProtocolInvalidValueError(BaseValidationError):
    """Raised when internet protocol is wrong value"""

# Transport protocol
class TransportProtocolInvalidFormatError(BaseValidationError):
    """Raised when transport protocol is wrong format"""

class TransportProtocolInvalidValueError(BaseValidationError):
    """Raised when transport protocol is wrong value"""

# Cast type
class CastTypeInvalidFormatError(BaseValidationError):
    """Raised when cast type is wrong format"""

class CastTypeInvalidValueError(BaseValidationError):
    """Raised when cast type is wrong value"""

# Seed
class SeedInvalidTypeError(BaseValidationError):
    """Raised when seed is wrong type"""

class SeedInvalidFormatError(BaseValidationError):
    """Raised when seed is wrong format"""

class SeedInvalidValueError(BaseValidationError):
    """Raised when seed is wrong value"""

#--- GENERIC TYPE EXCEPTIONS----
# String
class StringTooLongError(BaseValidationError):
    """Raised when a string is too long"""

class StringTooShortError(BaseValidationError):
    """Raised when a string is too short"""

class StringInvalidFormatError(BaseValidationError):
    """Raised when a string is wrong format"""

# Integer
class IntegerInvalidTypeError(BaseValidationError):
    """Raised when an integer is wrong type"""

class IntegerInvalidFormatError(BaseValidationError):
    """Raised when an integer is wrong format"""

class IntegerTooLargeError(BaseValidationError):
    """Raised when an integer is too large"""

class IntegerTooSmallError(BaseValidationError):
    """Raised when an integer is too small"""

class IntegerMustBePositiveError(BaseValidationError):
    """Raised when an integer should be but is not positive"""

class IntegerMustBeNegativeError(BaseValidationError):
    """Raised when an integer should but is not negative"""
