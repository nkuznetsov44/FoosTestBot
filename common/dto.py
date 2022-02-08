from typing import Union, Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime
from common.model import TelegramUser, TestSession, Answer
from common.questions import questions, FoosTestQuestionBase


@dataclass_json
@dataclass(frozen=True)
class UserDto:
    user_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]

    @staticmethod
    def from_model(user: TelegramUser) -> 'UserDto':
        return UserDto(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
        )


@dataclass_json
@dataclass(frozen=True)
class TestSessionDto:
    id: int
    user: UserDto
    start_time: datetime
    end_time: Optional[datetime]
    score: Optional[int]
    is_checked: bool

    @staticmethod
    def from_model(test_session: TestSession) -> 'TestSessionDto':
        return TestSessionDto(
            id=test_session.id,
            user=UserDto.from_model(test_session.user),
            start_time=test_session.start_time,
            end_time=test_session.end_time,
            score=test_session.score,
            is_checked=test_session.is_checked,
        )


@dataclass_json
@dataclass(frozen=True)
class QuestionDto:
    code: str
    text: str
    text_with_enumeration: str
    correct_answer_index: Optional[int]
    correct_answer_text: str

    @staticmethod
    def from_question(question: FoosTestQuestionBase) -> 'QuestionDto':
        return QuestionDto(
            code=question.question,
            text=question.text,
            text_with_enumeration=question.text_with_enumeration,
            correct_answer_index=question.correct_answer_index,
            correct_answer_text=question.correct_answer,
        )


@dataclass_json
@dataclass(frozen=True)
class AnswerDto:
    id: int
    test_session: TestSessionDto
    question: QuestionDto
    answer: Union[int, str]
    is_correct: Optional[bool]

    @staticmethod
    def from_model(answer: Answer) -> 'AnswerDto':
        return AnswerDto(
            id=answer.id,
            test_session=TestSessionDto.from_model(answer.test_session),
            question=QuestionDto.from_question(questions[answer.question]),
            answer=answer.answer,
            is_correct=answer.is_correct,
        )
