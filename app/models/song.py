import enum

from sqlalchemy_utils import UUIDType

from .base import BaseModel
from app.database import db


class SongStatus(enum.Enum):
    normal = 'normal'
    liked = 'liked'
    removed = 'removed'


class Song(BaseModel):
    __tablename__ = 'song'

    artist = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    playlist_id = db.Column(UUIDType(binary=False), db.ForeignKey('playlist.id'), unique=False, index=True)
    status = db.Column(db.Enum(SongStatus), nullable=False)
