class ApplicationException(Exception):
    pass


class DatabaseException(ApplicationException):
    pass


class AwsException(ApplicationException):
    pass


class ApiException(ApplicationException):
    pass


class SteamApiException(ApiException):
    pass
