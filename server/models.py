from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, DateTime, func
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    body = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    def __repr__(self) -> str:
        return f"<Message: {self.body}"

