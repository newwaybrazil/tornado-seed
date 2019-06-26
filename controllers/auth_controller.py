"""
AuthController module.
It contains all the permission controller-related functions.
"""

import tornado
from tornado.escape import json_decode

from controllers.base_controller import BaseController
from services.user_service import UserService
from models.user import User
from core.access_control import hash_password


class AuthController(BaseController):
    """
    AuthController class.
    """

    LOGIN = 'login'
    LOGOUT = 'logout'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user_service = UserService(self.db, self.config)

    async def post(self, method: str=None):
        if method == self.LOGIN:
            auth = self.get_json_body()
            password = auth["password"]
            username = auth["username"]
            user, token = await self.user_service.authenticate(username, password)
            self.write({
                'user': user,
                'token': token
            })
            self.finish()
        
