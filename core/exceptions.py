class BaseHttpException(Exception):
    STATUS_CODE = 500
    MESSAGE = 'Server Error'

    def __init__(self, status_code: int = None, message: str = None):
        if status_code:
            self.STATUS_CODE = status_code
        if message:
            self.MESSAGE = message

class AuthorizationException(BaseHttpException):
    STATUS_CODE = 403
    MESSAGE = 'acesso não permitido'


class AuthenticationException(BaseHttpException):
    STATUS_CODE = 401
    MESSAGE = 'autenticação necessária'
