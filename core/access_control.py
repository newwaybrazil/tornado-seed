import logging
from core.exceptions import AuthorizationException
import hashlib


def hash_password(password):
    h = hashlib.sha256(password.encode())
    return h.hexdigest()


def _check_rules(token_payload, roles: list=None):
    min_permission = min(roles)
    if token_payload.get('role', 0) <= min_permission:
        raise AuthorizationException()


def authorization(roles: list=None):
    if not roles:
        roles = []

    methods = [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ]

    def class_rebuilder(cls):
        class Wrapper(cls):
            """ Decorated class """

            def __getattribute__(self, attr_name):
                obj = super().__getattribute__(attr_name)
                if hasattr(obj, '__call__') and attr_name in methods:
                    try:
                        token, token_payload = super().get_authorization()
                        if token != super().get_root_token():
                            _check_rules(token_payload, roles)
                            return obj
                        else:
                            return obj

                    except AuthorizationException as e:
                        logging.exception(e)
                        super().set_status(401)
                        super().write({
                            'error': 'Unauthorized'
                        })
                        super().finish()
                        return
                else:
                    return obj

        return Wrapper

    return class_rebuilder
