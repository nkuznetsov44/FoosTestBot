from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from settings import database_uri
from model import TelegramUser


app = Flask(__name__)
db_engine = create_engine(database_uri, pool_recycle=3600)
DbSession = scoped_session(sessionmaker(bind=db_engine))


@app.route('/api/users')
def users():
    db_session = DbSession()
    try:
        users = db_session.query(TelegramUser).all()
        return jsonify(TelegramUser.serialize_list(users))
    finally:
        DbSession.remove()
