#--- BASE EXCEPTIONS----
# Base Validation Class
class BaseValidationError(ValueError):
    pass

#--- SPECIFIC EXCEPTIONS----
# IP address
class IpAddressInvalidFormatError(BaseValidationError):
    pass
class IpAddressInvalidValueError(BaseValidationError):
    pass
class IpScopeAddressInvalidValueError(BaseValidationError):
    pass

# Mac address
class MacAddressInvalidFormatError(BaseValidationError):
    pass
class MacAddressInvalidValueError(BaseValidationError):
    pass

# Port
class PortInvalidFormatError(BaseValidationError):
    pass
class PortInvalidValueError(BaseValidationError):
    pass

# Name
class NameTooLongError(BaseValidationError):
    pass
class NameTooShortError(BaseValidationError):
    pass
class NameInvalidFormatError(BaseValidationError):
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

# Cast type
class CastTypeInvalidFormatError(BaseValidationError):
    pass
class CastTypeInvalidValueError(BaseValidationError):
    pass

#--- GENERIC EXCEPTIONS----
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
