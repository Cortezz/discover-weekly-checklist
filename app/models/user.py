from flask_login import UserMixin

from app.database import db
from .base import BaseModel
from app.models.playlist import Playlist
from app.models.token import Token


class User(BaseModel, UserMixin):
    __tablename__ = 'user'

    name = db.Column(db.String, nullable=False)
    spotify_id = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    playlists = db.relationship(Playlist)
    token = db.relationship(Token, uselist=False)
