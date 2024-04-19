import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    desc = sqlalchemy.Column(sqlalchemy.String)
    prev = sqlalchemy.Column(sqlalchemy.String)
    file = sqlalchemy.Column(sqlalchemy.String)
    author = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    rate = sqlalchemy.Column(sqlalchemy.Float)
    votes = sqlalchemy.Column(sqlalchemy.Integer)
    images = orm.relationship("Image")
