DEP_ERROR_MSG = "%s has been immediately deprecated."


class IEXSymbolError(Exception):
    """
    This error is thrown when an invalid symbol is given.
    """

    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return "Symbol " + self.symbol + " not found."


class IEXQueryError(Exception):
    """
    This error is thrown when an error occurs with the query to IEX, be it a
    network problem or an invalid query.
    """
    _DEFAULT_MSG = "The query could not be completed. There was a " \
                   "client-side error with your request."

    def __init__(self, message=None):
        self.message = message or self._DEFAULT_MSG

    def __str__(self):
        return self.message


class IEXAuthenticationError(Exception):
    """
    This error is thrown when there is an authentication issue with an IEX
    cloud request.
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ImmediateDeprecationError(Exception):

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def __str__(self):
        return DEP_ERROR_MSG % self.endpoint
