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


@app.route('/api/answers/checked/<int:test_session_id>', methods=['POST'])
def answers_checked(test_session_id: int) -> Response:
    request_data = request.get_json()
    checked_answers = {answer['id']: answer['is_correct'] for answer in request_data}
    foos_test_service.process_checked_answers(test_session_id, checked_answers)
    return Response(status=200)
