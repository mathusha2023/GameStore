import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "comments"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("games.id"))
    user = sqlalchemy.Column(sqlalchemy.Integer)
    mark = sqlalchemy.Column(sqlalchemy.Integer)
    message = sqlalchemy.Column(sqlalchemy.String)
