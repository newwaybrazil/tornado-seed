from datetime import datetime, timedelta

import jwt

from core.access_control import hash_password
from core.exceptions import AuthenticationException
from models.user import User


class UserService():
    def __init__(self, db, config):
        self.db = db
        self.config = config
        self.user = User(self.db)

    async def register(self, username: str=None,
                       password: str=None,
                       role: int=100,
                       password_hashed: bool=False):
        new_user = {
            'username': username,
            'password': password if password_hashed else hash_password(password),
            'role': role
        }
        saved = await self.user.save(new_user)
        return saved
  
    async def authenticate(self, username, password):
        user_found = await self.user.first({
            'username': username,
            'password': hash_password(password)
        })

        if not user_found:
            raise AuthenticationException()

        token = await self._generate_token(user_obj=user_found)

        return user_found, token

    async def _generate_token(self, user_obj: User=None, user_id: str=None):
        if not user_obj and user_id:
            user_obj = await self.user.first({'_id': user_id})
        if not user_obj:
            raise Exception('Missing user/user_id')

        payload = {
            'username': user_obj.get('username'),
            'name': user_obj.get('name'),
            'role': user_obj.get('role'),
            'exp': datetime.utcnow() + timedelta(hours=8)
        }

        key = self.config.api['secret']

        return jwt.encode(payload, key, algorithm='HS256').decode()
