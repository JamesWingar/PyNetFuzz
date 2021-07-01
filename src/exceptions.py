#--- BASE EXCEPTIONS----
# Base Validation Class
class BaseValidationError(ValueError):
    pass

#--- CLASS EXCEPTIONS----
class InvalidHostError(BaseValidationError):
    pass
class InvalidPacketError(BaseValidationError):
    pass
class InvalidRandomiserError(BaseValidationError):
    pass

#--- HOST EXCEPTIONS----
class HostNoIpAddressError(BaseValidationError):
    pass
class HostNoMacAddressError(BaseValidationError):
    pass
class HostNoPortAddressError(BaseValidationError):
    pass
class HostGetLocalIpError(BaseValidationError):
    pass
class HostGetLocalMacError(BaseValidationError):
    pass
class HostGetRemoteMacError(BaseValidationError):
    pass

#--- PACKET EXCEPTIONS----
class PacketInfoTypeError(BaseValidationError):
    pass
class PacketInfoKeysError(BaseValidationError):
    pass
class PacketInfoLengthError(BaseValidationError):
    pass
class PacketInfoMissingEntriesError(BaseValidationError):
    pass
class PacketInfoExtraEntriesError(BaseValidationError):
    pass

#--- RANDOMISER EXCEPTIONS----


#--- VALIDATION EXCEPTIONS----
# IP address
class IpAddressInvalidTypeError(BaseValidationError):
    pass
class IpAddressInvalidFormatError(BaseValidationError):
    pass
class IpScopeAddressInvalidFormatError(BaseValidationError):
    pass
class IpAddressInvalidValueError(BaseValidationError):
    pass
class IpScopeAddressInvalidValueError(BaseValidationError):
    pass
class IpAddressTooLongValueError(BaseValidationError):
    pass
class IpAddressTooShortValueError(BaseValidationError):
    pass

# Mac address
class MacAddressInvalidTypeError(BaseValidationError):
    pass
class MacAddressInvalidFormatError(BaseValidationError):
    pass
class MacAddressInvalidValueError(BaseValidationError):
    pass
class MacAddressTooLongValueError(BaseValidationError):
    pass
class MacAddressTooShortValueError(BaseValidationError):
    pass

# Port
class PortInvalidTypeError(BaseValidationError):
    pass
class PortInvalidFormatError(BaseValidationError):
    pass
class PortInvalidValueError(BaseValidationError):
    pass

# Name
class NameInvalidTypeError(BaseValidationError):
    pass
class NameInvalidFormatError(BaseValidationError):
    pass
class NameInvalidValueError(BaseValidationError):
    pass
class NameTooLongError(BaseValidationError):
    pass
class NameTooShortError(BaseValidationError):
    pass

# Internet protocol
class InternetProtocolInvalidFormatError(BaseValidationError):
    pass
class InternetProtocolInvalidValueError(BaseValidationError):
    pass

# Transport protocol
class TransportProtocolInvalidFormatError(BaseValidationError):
    pass
class TransportProtocolInvalidValueError(BaseValidationError):
    pass

# Cast type
class CastTypeInvalidFormatError(BaseValidationError):
    pass
class CastTypeInvalidValueError(BaseValidationError):
    pass

# Seed
class SeedInvalidTypeError(BaseValidationError):
    pass
class SeedInvalidFormatError(BaseValidationError):
    pass
class SeedInvalidValueError(BaseValidationError):
    pass

#--- GENERIC TYPE EXCEPTIONS----
# String
class StringTooLongError(BaseValidationError):
    pass
class StringTooShortError(BaseValidationError):
    pass
class StringInvalidFormatError(BaseValidationError):
    pass

# Integer
class IntegerTooLargeError(BaseValidationError):
    pass
class IntegerTooSmallError(BaseValidationError):
    pass
class IntegerInvalidFormatError(BaseValidationError):
    pass
class IntegerMustBePositiveError(BaseValidationError):
    pass
class IntegerMustBeNegativeError(BaseValidationError):
    pass
