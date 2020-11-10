DEP_ERROR_MSG = "%s has been immediately deprecated."


class IEXQueryError(Exception):
    """
    This error is thrown when an error occurs with the query to IEX, be it a
    network problem or an invalid query.
    """

    _DEFAULT_MSG = (
        "The query could not be completed. There was a "
        "client-side error with your request."
    )

    def __init__(self, status, response):
        self.response = response
        self.status = status

    def __str__(self):
        return "An error occurred while making the query ({}): {}".format(
            self.status, self.response
        )


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
