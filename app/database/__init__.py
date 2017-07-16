from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_tables():
    from app.models.token import Token
    from app.models.user import User

    db.create_all()


def drop_tables():
    db.reflect()
    db.drop_all()
