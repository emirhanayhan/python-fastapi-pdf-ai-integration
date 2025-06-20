
class AppException(Exception):
    def __init__(self, error_message, error_code, status_code):
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = status_code
