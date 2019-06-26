"""
UserController module.
It contains all the permission controller-related functions.
"""

import tornado
from tornado.escape import json_decode

from controllers.base_controller import BaseController
from models.user import User
from services.user_service import UserService
from core.access_control import authorization, hash_password
from core.enumerators import AppEnum


@authorization(roles=[AppEnum.ROOT_PERMISSION])
class UserController(BaseController):
    """
    UserController class.
    """

    def __init__(self, *args, **kwargs):
        kwargs['model'] = User
        super().__init__(*args, **kwargs)
        self.user_service = UserService(self.db, self.config)

    async def get(self, model_id: str = None):
        single_result = False
        criteria = self.get_clean_arguments()

        if model_id is not None:
            if model_id == "paged":
                await self.paged(criteria, criteria, [])
                return
            else:
                criteria["_id"] = model_id
                single_result = True

        r = await self.user.find(criteria, single_result, [])
        if single_result:
            self.write(r)
        else:
            self.write({"results": r})

    async def paged(self, params, pagination, relations: list = []):
        r = await self.user.paged(params, pagination, relations)
        if r:
            self.write(r)
        else:
            self.write({})

    async def post(self, model_id: str=None):
        to_save = self.get_json_body()
        saved = await self.user_service.register(**to_save)
        self.write(saved)
