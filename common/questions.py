from typing import List, Optional


class FoosTestQuestionBase:
    def __init__(self, number: int, question: str) -> None:
        self._number = number
        self._question = question

    @property
    def text(self) -> str:
        return self._question

    @property
    def text_with_enumeration(self) -> str:
        return f'Вопрос {self._number} из {TOTAL_QUESTIONS}:\n{self._question}'

    @property
    def question(self) -> str:
        return f'q{self._number}'

    @property
    def correct_answer_index(self) -> Optional[int]:
        raise NotImplementedError()

    @property
    def correct_answer(self) -> str:
        raise NotImplementedError()


class FoosTestOpenQuestion(FoosTestQuestionBase):
    def __init__(self, number: int, question: str, correct_answer: str) -> None:
        super().__init__(number, question)
        self._correct_answer = correct_answer

    @property
    def correct_answer_index(self) -> Optional[int]:
        return None

    @property
    def correct_answer(self) -> str:
        return self._correct_answer


class FoosTestQuestion(FoosTestQuestionBase):
    def __init__(self, number: int, question: str, options: List[str], correct_answer_index: int) -> None:
        super().__init__(number, question)
        self._options = options
        self._correct_answer_index = correct_answer_index

    @property
    def options(self) -> List[str]:
        return self._options

    @property
    def correct_answer_index(self) -> int:
        return self._correct_answer_index

    @property
    def correct_answer(self) -> str:
        return self._options[self.correct_answer_index]


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
        options=['Да', 'Нет'],
        correct_answer_index=1,
    ),
    'q2': FoosTestQuestion(
        number=2,
        question=(
            'Прокручивание неудерживаемой Игроком штанги в результате удара мяча по фигурке '
            'игрока не является нарушением'
        ),
        options=['Да', 'Нет'],
        correct_answer_index=0,
    ),
    'q3': FoosTestQuestion(
        number=3,
        question=(
            'Разрешается оспорить решение Арбитра в случае, если оно касается трактовки правил.'
        ),
        options=['Да', 'Нет'],
        correct_answer_index=0,
    ),
    'q4': FoosTestQuestion(
        number=4,
        question=(
            'Если мяч покинул пределы стола, он вводится в игру путем подачи тем, кто '
            'изначально подавал этот мяч'
        ),
        options=['Да', 'Нет'],
        correct_answer_index=1,
    ),
    'q5': FoosTestQuestion(
        number=5,
        question='Сотрясения аккумулируются на протяжении матча.',
        options=['Да', 'Нет'],
        correct_answer_index=0,
    ),
    'q6': FoosTestQuestion(
        number=6,
        question='Сбросы аккумулируются на протяжении матча.',
        options=['Да', 'Нет'],
        correct_answer_index=1,
    ),
    'q7': FoosTestQuestion(
        number=7,
        question=(
            'Прижатый или остановленный мяч, отправленный со 2-й линии, разрешается поймать '
            'на 3-й линии, если после отправления с линии он коснулся игрока 2-й линии '
            'противника.'
        ),
        options=['Да', 'Нет'],
        correct_answer_index=1,
    ),
    'q8': FoosTestQuestion(
        number=8,
        question=(
            'Прижатый или остановленный мяч, отправленный с 1-й линии, разрешается поймать '
            'на 2-й линии, если после отправления с линии он коснулся игрока 3-й линии '
            'противника.'
        ),
        options=['Да', 'Нет'],
        correct_answer_index=0,
    ),
    'q9': FoosTestQuestion(
        number=9,
        question=(
            'Объявление сброса на 2-й линии также сбрасывает число касаний мячом стенок стола'
        ),
        options=['Да', 'Нет'],
        correct_answer_index=0,
    ),
    'q10': FoosTestQuestion(
        number=10,
        question=(
            'Если пенальти завершается взятием ворот, мяч подает команда, пропустившая гол.'
        ),
        options=['Да', 'Нет'],
        correct_answer_index=0,
    ),
    'q11': FoosTestQuestion(
        number=11,
        question='Какое наказание предусмотрено за получение третьего тайм-аута за одну игру?',
        options=['Предупреждение', 'Потеря владения', 'Технический фол'],
        correct_answer_index=2,
    ),
    'q12': FoosTestQuestion(
        number=12,
        question=(
            'После тайм-аута команда, подающая мяч, теряет его до касания второй фигуркой игрока. '
            'Как может распорядиться мячом ненарушившая команда?'
        ),
        options=[
            'Ввести мяч в игру с 1-й линии',
            'Ввести мяч в игру путем подачи',
            'Продолжить игру из текущей позиции или подать мяч'
        ],
        correct_answer_index=2,
    ),
    'q13': FoosTestQuestion(
        number=13,
        question='Какое наказание предусмотрено за умышленную остановку мяча в мертвой зоне?',
        options=[
            'Предупреждение',
            'Подача мяча противником',
            'Технический фол'
        ],
        correct_answer_index=1,
    ),
    'q14': FoosTestQuestion(
        number=14,
        question=(
            'Защитник пробивает постановочный удар, который попадает в ворота противников, отскочив от '
            'фигурки игрока на 2-й линии его партнера. Как расценивается такая ситуация с точки зрения '
            'правил?'
        ),
        options=[
            'Пас не по правилам (остановленный мяч) – Гол не засчитывается – Подача противников.',
            'Нет нарушения – Гол засчитывается.',
            'Пас не по правилам (остановленный мяч) – Гол не засчитывается – Противник вводит мяч с 1-й линии.'
        ],
        correct_answer_index=1,
    ),
    'q15': FoosTestQuestion(
        number=15,
        question='Какое наказание предусмотрено за повторное нарушение правил разминки?',
        options=[
            'Предупреждение',
            'Подача мяча противником',
            'Технический фол'
        ],
        correct_answer_index=2,
    ),
    'q16': FoosTestQuestion(
        number=16,
        question='Какое наказание предусмотрено за первое сотрясение?',
        options=[
            'Предупреждение',
            'На выбор противника: продолжение игры или его подача',
            'Технический фол'
        ],
        correct_answer_index=1,
    ),
    'q17': FoosTestQuestion(
        number=17,
        question=(
            'Какое наказание предусмотрено за попытки умышленного сброса своего партнера с целью '
            'добиться объявления сброса Арбитром?'
        ),
        options=[
            'Предупреждение',
            'Потеря владения',
            'Технический фол'
        ],
        correct_answer_index=1,
    ),
    'q18': FoosTestQuestion(
        number=18,
        question=(
            'Нападающий зажимает мяч на 2-й линии и бьет по воротам той же фигуркой игрока. Мяч '
            'попадает в игрока его 3-й линии, и он инстинктивно бьет им по мячу, с трудом попадая в ворота '
            'косым ударом. Как расценивается такая ситуация с точки зрения правил?'
        ),
        options=[
            'Пас не по правилам (остановленный мяч) – Гол не засчитывается – Подача противников.',
            'Пас не по правилам (остановленный мяч) – Гол не засчитывается – Противник вводит мяч с 1-й линии',
            'Нет нарушения – Гол засчитывается'
        ],
        correct_answer_index=0,
    ),
    'q19': FoosTestQuestion(
        number=19,
        question='При подаче или при вводе мяча в игру после тайм-аута отсчет времени владения начинается',
        options=[
            'как только мяч касается второй фигурки игрока',
            'через одну секунду после того, как мяч касается второй фигурки игрока',
            'как только мяч сдвигается с места'
        ],
        correct_answer_index=1,
    ),
    'q20': FoosTestQuestion(
        number=20,
        question='Объявлен судейский тайм-аут. Разрешается поменяться позициями с партнером',
        options=[
            'при любых обстоятельствах',
            'только взяв тайм-аут',
            'только если это разрешалось бы сделать, если бы не был объявлен судейский тайм-аут'
        ],
        correct_answer_index=2,
    ),
    'q21': FoosTestOpenQuestion(
        number=21,
        question=(
            'Ответы на открытые вопросы (без вариантов ответа) просто пишите в сообщении. '
            'Изменить такие ответы будет нельзя. Вы все еще можете переголосовать в вопросах с вариантами ответов.\n'
            'Каково разрешенное время владения на 1-й линии?'
        ),
        correct_answer='15 секунд',
    ),
    'q22': FoosTestOpenQuestion(
        number=22,
        question='Каково разрешенное время владения на 2-й линии?',
        correct_answer='10 секунд',
    ),
    'q23': FoosTestOpenQuestion(
        number=23,
        question='Каково разрешенное время владения на 3-й линии?',
        correct_answer='15 секунд',
    ),
    'q24': FoosTestOpenQuestion(
        number=24,
        question='Каково разрешенное время тайм-аута?',
        correct_answer='30 секунд',
    ),
    'q25': FoosTestOpenQuestion(
        number=25,
        question='Каково разрешенное время промежутка между играми?',
        correct_answer='90 секунд',
    ),
    'q26': FoosTestOpenQuestion(
        number=26,
        question=(
            'Изначально мяч подавала команда А. С какой линии мяч вводится в игру после того, как '
            'он остановился в мертвой зоне между 2-ми линиями?'
        ),
        correct_answer='Средняя линия команды А',
    ),
    'q27': FoosTestOpenQuestion(
        number=27,
        question=(
            'Изначально мяч подавала команда А. С какой линии мяч вводится в игру после того, как '
            'он остановился в мертвой зоне рядом с 3-й линией команды Б?'
        ),
        correct_answer='Линия защиты команды А',
    ),
    'q28': FoosTestOpenQuestion(
        number=28,
        question=(
            'Изначально мяч подавала команда А. С какой линии мяч вводится в игру после того, как '
            'он остановился в мертвой зоне защитника команды А?'
        ),
        correct_answer='Линия защиты команды А',
    ),
    'q29': FoosTestOpenQuestion(
        number=29,
        question=(
            'Изначально мяч подавала команда А. С какой линии мяч вводится в игру после того, как '
            'он был выброшен за пределы стола игроком команды Б?'
        ),
        correct_answer='Линия защиты команды А',
    ),
    'q30': FoosTestOpenQuestion(
        number=30,
        question=(
            'Это последний вопрос. После ответа на него смена голосов в опросах не будет засчитана.\n'
            'Изначально мяч подавала команда А. С какой линии мяч вводится в игру после того, как '
            'команда А превысила время владения на 3-й линии?'
        ),
        correct_answer='Линия защиты команды B',
    ),
}


TOTAL_QUESTIONS = len(questions.keys())
