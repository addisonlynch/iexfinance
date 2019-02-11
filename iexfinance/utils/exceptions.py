class IEXSymbolError(Exception):
    """
    This error is thrown when an invalid symbol is given.
    """
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return "Symbol " + self.symbol + " not found."


class IEXEndpointError(Exception):
    """
    This error is thrown when an invalid endpoint is specified in the custom
    endpoint lookup method
    """
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def __str__(self):
        return "Endpoint " + self.endpoint + " not found."


class IEXFieldError(Exception):
    """
    This error is thrown when an invalid field is specified in the custom
    endpoint lookup method
    """
    def __init__(self, endpoint, field):
        self.field = field
        self.endpoint = endpoint

    def __str__(self):
        return ("Field " + self.field + " not found in Endpoint " +
                self.endpoint)


class IEXQueryError(Exception):
    """
    This error is thrown when an error occurs with the query to IEX, be it a
    network problem or an invalid query.
    """
    def __str__(self):
        return "An error occurred while making the query."


class IEXAuthenticationError(Exception):
    """
    This error is thrown when there is an authentication issue with an IEX
    cloud request.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class IEXVersionError(Exception):
    """
    This error is thrown when an attempt is made to access an IEX Cloud
    endpoint when API version 1 (v1) has been selected for use.
    """
    def __init__(self, version):
        self.version = version

    def __str__(self):
        msg = "The requested endpoint is only available using %s."
        return msg % self.version
