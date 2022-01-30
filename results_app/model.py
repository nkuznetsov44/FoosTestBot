from typing import Any, List, Dict
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


class Serializable:
    def serialize(self) -> Dict[str, Any]:
        raise NotImplementedError()


class SerializeListMixin:
    @staticmethod
    def serialize_list(lst: List[Any]) -> List[Dict[str, Any]]:
        return [obj.serialize() for obj in lst]


Base = declarative_base()


class TelegramUser(Base, Serializable, SerializeListMixin):
    __tablename__ = 'telegram_user'

    user_id = Column('user_id', Integer, primary_key=True)
    first_name = Column('first_name', String, nullable=True)
    last_name = Column('last_name', String, nullable=True)
    username = Column('username', String, nullable=True)
    answers = relationship('Answer')

    def serialize(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username
        }


class Answer(Base, Serializable, SerializeListMixin):
    __tablename__ = 'answers'

    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('telegram_user.user_id'))
    user = relationship('TelegramUser', back_populates='answers')
    question = Column('question', String)
    answer = Column('answer', Text, nullable=True)
    answer_time = Column('answer_time', DateTime)

    def serialize(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question': self.question,
            'answer': self.answer,
            'answer_time': self.answer_time
        }
