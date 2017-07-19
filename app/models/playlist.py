from sqlalchemy_utils import UUIDType

from .base import BaseModel
from app.database import db


class Playlist(BaseModel):
    __tablename__ = 'playlist'

    spotify_id = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(UUIDType(binary=False), db.ForeignKey('user.id'), nullable=False, index=True, unique=False)
