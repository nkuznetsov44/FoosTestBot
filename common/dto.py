from typing import Union, Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime
from common.model import Answer
from common.questions import questions, FoosTestQuestion


@dataclass_json
@dataclass(frozen=True)
class AnswerDto:
    id: int
    user_id: int
    question: str
    question_text: str
    answer: Union[int, str]
    correct_answer_index: Optional[int]
    correct_answer: Optional[str]
    is_correct: Optional[bool]
    answer_time: datetime

    @staticmethod
    def from_model(answer: Answer) -> 'AnswerDto':
        question = questions[answer.question]
        return AnswerDto(
            id=answer.id,
            user_id=answer.user_id,
            question=question.question,
            question_text=question.text,
            answer=answer.answer,
            correct_answer_index=question.correct_answer_index,
            correct_answer=question.correct_answer,
            is_correct=answer.is_correct,
            answer_time=answer.answer_time
        )
