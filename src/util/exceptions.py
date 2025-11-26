
"""
exceptions.py — defines custom exception classes used throughout the application
to handle specific Terma agent exceptions.
"""


class ConfigurationException(Exception):
    """
    :exception: raised when Terma's configuration is invalid during prompt processing
    """


class ProviderException(Exception):
    """
    :exception: raised when Terma's provider is invalid during prompt processing
    """


class AuthenticationException(Exception):
    """
    :exception: raised when authentication for the provider fails during prompt processing
    """
