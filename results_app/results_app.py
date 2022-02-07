from flask import Flask, jsonify, Response, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from settings import database_uri
from common.model import TelegramUser, Answer


app = Flask(__name__)
db_engine = create_engine(database_uri, pool_recycle=3600)
DbSession = scoped_session(sessionmaker(bind=db_engine))


@app.route('/api/users', methods=['GET'])
def users() -> Response:
    db_session = DbSession()
    try:
        users = db_session.query(TelegramUser).all()
        return jsonify(TelegramUser.serialize_list(users))
    finally:
        DbSession.remove()


@app.route('/api/answers/<int:user_id>', methods=['GET'])
def answers(user_id: int) -> Response:
    db_session = DbSession()
    try:
        answers = db_session.query(Answer).filter(Answer.user_id == user_id)
        return jsonify(Answer.serialize_list(answers))
    finally:
        DbSession.remove()


@app.route('/api/answers/changes', methods=['POST'])
def answers_changes() -> Response:
    request_data = request.get_json()
    db_session = DbSession()
    try:
        for answer_change in request_data:
            answer = db_session.query(Answer).get(answer_change['id'])
            answer.is_correct = answer_change['is_correct']
        db_session.commit()
    finally:
        DbSession.remove()
    return Response(status=200)
