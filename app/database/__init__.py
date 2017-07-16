from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_tables():
    from app.models.user import User
    from app.models.token import Token

    db.create_all()


def drop_tables():
    db.drop_all()
