import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "games"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    desc = sqlalchemy.Column(sqlalchemy.String)
    prev = sqlalchemy.Column(sqlalchemy.String)
    file = sqlalchemy.Column(sqlalchemy.String)
    author = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    rate = sqlalchemy.Column(sqlalchemy.Float)
    images = orm.relationship("Image")
    comments = orm.relationship("Comment")

    def update_rate(self):
        self.rate = round(sum([comment.mark for comment in self.comments]) / len(self.comments), 1)
