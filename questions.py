from typing import List
from dataclasses import dataclass


@dataclass(frozen=True)
class FoosTestQuestion:
    question: str
    options: List[str]


TOTAL_QUESTIONS = 3


def get_question(question: str) -> FoosTestQuestion:
    if question == 'q1':
        return q1
    if question == 'q2':
        return q2
    if question == 'q3':
        return q3
    raise ValueError(f'Unknown question {question}')


def _format_question(number, question) -> str:
    return f'Вопрос {number} из {TOTAL_QUESTIONS}:\n{question}'


q1 = FoosTestQuestion(
    question=_format_question(1, 'Наказание за запрос третьего тайм-аута – технический фол.'),
    options=['Да', 'Нет']
)

q2 = FoosTestQuestion(
    question=_format_question(2, 'Какое наказание предусмотрено за получение третьего тайм-аута за одну игру?'),
    options=['Предупреждение', 'Потеря владения', 'Технический фол']
)

q3 = FoosTestQuestion(
    question=_format_question(
        3,
        (
            'После тайм-аута команда, подающая мяч, теряет его до касания второй фигуркой игрока. '
            'Как может распорядиться мячом ненарушившая команда?'
        )
    ),
    options=[
        'Ввести мяч в игру с 1-й линии',
        'Ввести мяч в игру путем подачи',
        'Продолжить игру из текущей позиции или подать мяч'
    ]
)
