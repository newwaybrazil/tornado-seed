"""
User model factory.
This is a model module that instanciates a User.
"""

from odm.data_types import Relations, Types
from odm import BaseModel


class User(BaseModel):
    """
    User class.

    """

    def __init__(self, db):
        super().__init__(db)
        self.db = db

        self.collection_name = "users"
        self.fields = dict()
        self.fields["_id"] = Types.ObjectId
        self.fields["username"] = Types.String
        self.fields["password"] = Types.String
        self.fields["role"] = Types.Integer
        self.protected_fields = ["password"]       
        self.relations = {
            
        }
