"""
BaseController module.
It serves as a scope for all child controllers.
"""

import ast
import json
import logging
import traceback

import jwt
import tornado.web
from tornado.escape import json_encode

from core import exceptions
from core.enumerators import AppEnum
from core.exceptions import AuthenticationException
from models.user import User
from odm.serializers import ODMSerializer


class BaseController(tornado.web.RequestHandler):
    """
    BaseController class.
    """

    def initialize(self, **kwargs):
        """
        It initializes a controller.
        :return: There is no return for this function.
        """

        self.db = kwargs.get('db')
        self.config = kwargs.get('config')
        # Models
        self.user = User(self.db)

        # Servicesba

        self.root_permission = AppEnum.ROOT_PERMISSION
        self.json_serializer = ODMSerializer()

        self.user_valid = None

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers",
                        "x-requested-with, Authorization, Content-type")
        self.set_header('Access-Control-Allow-Methods',
                        'POST, GET, OPTIONS, PATCH, DELETE, PUT')

    def get_json_body(self):
        body = self.request.body
        if body:
            return tornado.escape.json_decode(body)
        else:
            return body

    def get_clean_arguments(self):
        """
        Cleans the arguments.

        :return: There is no return for this function.
        """
        criterion = {}
        for key, value in self.request.arguments.items():
            if len(value) == 1:
                param = value[0].decode()
                if param == "true":
                    param = True
                elif param == "false":
                    param = False
                elif "{" == param[0]:
                    param = json.loads(param)
                criterion[key] = param
            else:
                param = []
                for sub_value in value:
                    if sub_value.decode() == "true":
                        param.append(True)
                    elif sub_value.decode() == "false":
                        param.append(False)
                    elif "{" == sub_value.decode()[0]:
                        param.append(json.loads(sub_value.decode()))
                    else:
                        param.append(sub_value.decode())
                criterion[key] = param
        return self.build_query(criterion)

    def options(self, **kwargs):
        """
        Sets the options.

        :param kwargs: Additional arguments.
        :return: There is no return for this function.
        """
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers",
                        "x-requested-with, Authorization, Content-type")
        self.set_header('Access-Control-Allow-Methods',
                        'POST, GET, OPTIONS, PATCH, DELETE, PUT')
        self.set_status(200)
        self.write("ok")
        self.finish()

    def get_root_token(self):
        return self.config.api['root_token']

    def get_app_token(self):
        return self.config.api['secret']

    def get_authorization(self):
        token = self.get_token()
        try:
            key = self.config.api['root_token']
            if key == token:
                return token, {"role": 1000}
            else:
                payload = jwt.decode(token, key, algorithms=["HS256"])
                return token, payload
        except Exception as e:
            logging.exception(e)
            key = self.config.api['root_token']
            if token == key:
                return token, {"role": 1000}
            return "", {"role": -1}
            # raise AuthenticationException() from e

    def get_token(self) -> str:
        """
        Gets a token.

        :return: There is no return for this function.
        """
        self.token = self.request.headers.get("Authorization", " ").split(" ")[1]
        return self.token

    def build_query(self, criteria):
        """
        Build with clean arguments.

        :param criteria: Clean arguments
        :return: Query generated
        """
        if self.user_valid:
            method = self.request.method
            path = self.request.path.replace("/api/v1/", "").split("/")[0]
            return criteria
        else:
            return criteria

    def write_error(self, status_code, **kwargs):
        """
        Writes an error response.

        :param status_code: Error code.
        :param kwargs: Additional arguments.
        :return: There is no return for this function.
        """
        if self.get_status() < 400:
            status_code = 500

        error_class, error, trace = kwargs.get('exc_info')

        message = str(error)

        if isinstance(error, exceptions.BaseHttpException):
            if error.MESSAGE:
                message = error.MESSAGE
            else:
                message = str(error)

            if error.STATUS_CODE:
                status_code = error.STATUS_CODE

        msg = {
            'error': {
                'error_class': error_class.__name__,
                'status_code': status_code,
                'message': message
            }
        }

        if self.config.api.get('debug'):
            msg['error']['trace'] = traceback.format_tb(trace)

        self.set_status(status_code)
        self.write(msg)
        self.finish()

    def json_response(self, r):
        self.write(self.json_serializer.encode(r))
        self.set_header('Content-Type', 'application/json')
        self.finish()
