from typing import List, Dict, Union, Optional
import logging
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from common.model import TelegramUser, TestSession, Answer
from common.questions import questions, FoosTestQuestion, FoosTestOpenQuestion
from common.dto import UserDto, TestSessionDto, AnswerDto


logger = logging.getLogger(__name__)


class FoosTestService:
    def __init__(self, database_uri: str) -> None:
        self.db_engine = create_engine(database_uri, pool_recycle=3600)
        self.DbSession = scoped_session(sessionmaker(bind=self.db_engine))

    def get_user(self, user_id: int) -> Optional[UserDto]:
        db_session = self.DbSession()
        try:
            user = db_session.query(TelegramUser).get(user_id)
            if not user:
                return None
            return UserDto.from_model(user)
        finally:
            self.DbSession.remove()

    def list_users(self) -> List[UserDto]:
        db_session = self.DbSession()
        try:
            users = db_session.query(TelegramUser).all()
            return list(map(UserDto.from_model, users))
        finally:
            self.DbSession.remove()

    def create_user(
        self, user_id: int, first_name: Optional[str], last_name: Optional[str], username: Optional[str]
    ) -> UserDto:
        db_session = self.DbSession()
        try:
            user = TelegramUser(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
            )
            db_session.add(user)
            db_session.commit()
            logger.info(f'Created new user {user}')
            return UserDto.from_model(user)
        finally:
            self.DbSession.remove()

    def get_user_test_sessions(self, user_id: int) -> List[TestSessionDto]:
        db_session = self.DbSession()
        try:
            user = db_session.query(TelegramUser).get(user_id)
            return list(map(TestSessionDto.from_model, user.test_sessions))
        finally:
            self.DbSession.remove()

    def create_test_session_for_user(self, user_id: int) -> TestSessionDto:
        db_session = self.DbSession()
        try:
            user = db_session.query(TelegramUser).get(user_id)
            test_session = TestSession(
                user_id=user.user_id,
                start_time=datetime.now(),
                end_time=None,
                score=None,
            )
            db_session.add(test_session)
            db_session.commit()
            logger.info(f'Created test_session {test_session} at {test_session.start_time}')
            return TestSessionDto.from_model(test_session)
        finally:
            self.DbSession.remove()

    def end_test_session(self, test_session_id: int, answers: Dict[str, Union[int, str]]) -> TestSessionDto:
        db_session = self.DbSession()
        try:
            test_session = db_session.query(TestSession).get(test_session_id)
            answers = self._save_user_answers(test_session.id, answers)
            test_session.end_time = datetime.now()
            test_session.score = self._calculate_score(answers)
            db_session.commit()
            logger.info(f'Ended test session {test_session_id} at {test_session.end_time}')
            return TestSessionDto.from_model(test_session)
        finally:
            self.DbSession.remove()

    def get_test_session_answers(self, test_session_id: int) -> List[AnswerDto]:
        db_session = self.DbSession()
        try:
            test_session = db_session.query(TestSession).get(test_session_id)
            return list(map(AnswerDto.from_model, test_session.answers))
        finally:
            self.DbSession.remove()

    def check_answers(self, answers: Dict[str, Union[int, str]]) -> Dict[str, Optional[bool]]:
        res: Dict[str, Optional[bool]] = {}
        for question_code, answer in answers.items():
            question: Union[FoosTestQuestion, FoosTestOpenQuestion] = questions[question_code]
            answer_is_correct = None
            if isinstance(question, FoosTestQuestion):
                answer_is_correct = question.correct_answer_index == int(answer)
            res[question_code] = answer_is_correct
        return res

    def _calculate_score(self, answers: List[AnswerDto]) -> int:
        s = 0
        for answer in answers:
            if answer.is_correct:
                s += 1
        return s

    def _save_user_answers(self, test_session_id: int, answers: Dict[str, Union[int, str]]) -> List[AnswerDto]:
        ret: List[Answer] = []
        db_session = self.DbSession()
        try:
            logger.info(f'Saving test session id={test_session_id} answers {answers}')
            test_session = db_session.query(TestSession).get(test_session_id)
            checked_answers = self.check_answers(answers)
            for question_code in answers.keys():
                answer = Answer(
                    test_session_id=test_session.id,
                    question=question_code,
                    answer=answers[question_code],
                    is_correct=checked_answers[question_code]
                )
                db_session.add(answer)
                ret.append(answer)
            db_session.commit()
            logger.info(f'Saved test session id={test_session_id} answers')
            return list(map(AnswerDto.from_model, ret))
        finally:
            self.DbSession.remove()