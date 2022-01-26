class FailedToLoginException(Exception):
    def __init__(self, details: str):
        self.details = details


class NoDataFromServer(Exception):
    def __init__(self, details: str):
        self.details = details
