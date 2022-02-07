from flask import Flask, jsonify, Response, request
from common.service import FoosTestService
from settings import database_uri


app = Flask(__name__)
foos_test_service = FoosTestService(database_uri)


@app.route('/api/users', methods=['GET'])
def users() -> Response:
    return jsonify(foos_test_service.list_users())


@app.route('/api/testSessions/<int:user_id>', methods=['GET'])
def user_test_sessions(user_id: int) -> Response:
    return jsonify(foos_test_service.get_user_test_sessions(user_id))


@app.route('/api/answers/<int:test_session_id>', methods=['GET'])
def test_session_answers(test_session_id: int) -> Response:
    return jsonify(foos_test_service.get_test_session_answers(test_session_id))


"""
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
"""
