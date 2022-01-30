from flask import Flask, jsonify, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from settings import database_uri
from model import TelegramUser, Answer


app = Flask(__name__)
db_engine = create_engine(database_uri, pool_recycle=3600)
DbSession = scoped_session(sessionmaker(bind=db_engine))


@app.route('/api/users')
def users() -> Response:
    db_session = DbSession()
    try:
        users = db_session.query(TelegramUser).all()
        return jsonify(TelegramUser.serialize_list(users))
    finally:
        DbSession.remove()


@app.route('/api/answers/<int:user_id>')
def answers(user_id: int) -> Response:
    db_session = DbSession()
    try:
        answers = db_session.query(Answer).filter(Answer.user_id == user_id)
        return jsonify(Answer.serialize_list(answers))
    finally:
        DbSession.remove()
