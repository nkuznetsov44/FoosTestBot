from typing import List


class FoosTestQuestionBase:
    def __init__(self, number: int, question: str) -> None:
        self._number = number
        self._question = question

    @property
    def text(self) -> str:
        return f'Вопрос {self._number} из {TOTAL_QUESTIONS}:\n{self._question}'


class FoosTestOpenQuestion(FoosTestQuestionBase):
    pass


class FoosTestQuestion(FoosTestQuestionBase):
    def __init__(self, number: int, question: str, options: List[str]) -> None:
        super().__init__(number, question)
        self._options = options

    @property
    def options(self) -> List[str]:
        return self._options


def get_previous_question_code(question: str) -> str:
    question_number = int(question.replace('q', ''))
    if question_number == 1:
        raise ValueError('Cant get previous question for first question')
    return f'q{question_number - 1}'


def get_last_question_code() -> str:
    return list(questions.keys())[-1]


questions = {
    'q1': FoosTestQuestion(
        number=1,
        question='Наказание за запрос третьего тайм-аута – технический фол.',
        options=['Да', 'Нет']
    ),
    'q2': FoosTestQuestion(
        number=2,
        question='Какое наказание предусмотрено за получение третьего тайм-аута за одну игру?',
        options=['Предупреждение', 'Потеря владения', 'Технический фол']
    ),
    'q3': FoosTestQuestion(
        number=3,
        question=(
            'После тайм-аута команда, подающая мяч, теряет его до касания второй фигуркой игрока. '
            'Как может распорядиться мячом ненарушившая команда?'
        ),
        options=[
            'Ввести мяч в игру с 1-й линии',
            'Ввести мяч в игру путем подачи',
            'Продолжить игру из текущей позиции или подать мяч'
        ]
    ),
    'q4': FoosTestOpenQuestion(
        number=4,
        question=(
            'Изначально мяч подавала команда А. С какой линии мяч вводится в игру после того, как '
            'он остановился в мертвой зоне между 2-ми линиями?'
        )
    ),
    'q5': FoosTestOpenQuestion(
        number=5,
        question=(
            'Это последний вопрос. После ответа на него смена голосов в опросах не будет засчитана.\n'
            'Изначально мяч подавала команда А. С какой линии мяч вводится в игру после того, как '
            'он остановился в мертвой зоне рядом с 3-й линией команды Б?'
        )
    )
}


TOTAL_QUESTIONS = len(questions.keys())
