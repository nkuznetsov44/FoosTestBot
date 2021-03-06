from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class TelegramUser(Base):
    __tablename__ = 'telegram_user'

    user_id = Column('user_id', Integer, primary_key=True)
    first_name = Column('first_name', String, nullable=True)
    last_name = Column('last_name', String, nullable=True)
    username = Column('username', String, nullable=True)
    test_sessions = relationship('TestSession')


class TestSession(Base):
    __tablename__ = 'test_session'

    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('telegram_user.user_id'))
    user = relationship('TelegramUser', back_populates='test_sessions')
    start_time = Column('start_time', DateTime)
    end_time = Column('end_time', DateTime, nullable=True)
    score = Column('score', Integer, nullable=True)
    is_checked = Column('is_checked', Boolean)
    answers = relationship('Answer')


class Answer(Base):
    __tablename__ = 'answers'

    id = Column('id', Integer, primary_key=True)
    test_session_id = Column('test_session_id', Integer, ForeignKey('test_session.id'))
    test_session = relationship('TestSession', back_populates='answers')
    question = Column('question', String)
    answer = Column('answer', Text, nullable=True)
    is_correct = Column('is_correct', Boolean, nullable=True)
