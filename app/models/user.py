from app.database import db
from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    name = db.Column(db.String, nullable=False)
    spotify_id = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
