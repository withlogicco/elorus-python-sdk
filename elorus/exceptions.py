class Error(Exception):
    """Base class for other exceptions"""

    def __init__(self, message, response=None):
        self.message = message
        self.response = response

    def __str__(self) -> str:
        return f"Error code: {self.response.status_code}, Error message: {self.message}"


class AuthenticationError(Error):
    """Raised when there is an authentication error"""

    def __init__(self, message, response=None):
        super().__init__(message, response)


class AuthorizationError(Error):
    """Raised when there is an authorization error"""

    def __init__(self, message, response=None):
        super().__init__(message, response)


class BadRequestError(Error):
    """Raised when the request is bad"""

    def __init__(self, message, response=None):
        super().__init__(message, response)


class ThrottlingError(Error):
    """Raised when the rate limit is exceeded"""

    def __init__(self, message, response=None):
        super().__init__(message, response)
