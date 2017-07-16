from .base import BaseModel
from app.database import db

from sqlalchemy_utils import UUIDType


class Token(BaseModel):
    __tablename__ = 'token'

    access_token = db.Column(db.String(), nullable=False)
    token_type = db.Column(db.String(), nullable=False)
    scope = db.Column(db.String(), nullable=False)
    expires_in = db.Column(db.Integer(), nullable=False)
    refresh_token = db.Column(db.String(), nullable=False)
    user_id = db.Column(UUIDType(binary=False), db.ForeignKey('user.id'), nullable=False, index=True, unique=True)
