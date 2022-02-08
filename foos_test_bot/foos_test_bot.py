from typing import Union, Optional
import logging
from aiogram.types import Message, PollAnswer, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.utils.emoji import emojize
from app import dp, start_app, foos_test_service
from foostest import FoosTest
from common.questions import (
    questions, TOTAL_QUESTIONS, get_previous_question_code, get_last_question_code,
    FoosTestQuestion, FoosTestOpenQuestion
)
from common.dto import TestSessionDto


logger = logging.getLogger(__name__)

START_TEST = 'Начать тест'
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(START_TEST))

NEXT_QUESTION = 'Следующий вопрос'
question_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(NEXT_QUESTION))

END_TEST = 'Завершить тест'
end_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(END_TEST))

GET_RESULT = 'Обновить результат'
get_result_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(GET_RESULT))

questions_with_options_states = [
    FoosTest.q1, FoosTest.q2, FoosTest.q3, FoosTest.q4, FoosTest.q5, FoosTest.q6, FoosTest.q7, FoosTest.q8,
    FoosTest.q9, FoosTest.q10, FoosTest.q11, FoosTest.q12, FoosTest.q13, FoosTest.q14, FoosTest.q15, FoosTest.q16,
    FoosTest.q17, FoosTest.q18, FoosTest.q19, FoosTest.q20
]
open_questions_states = [
    FoosTest.q21, FoosTest.q22, FoosTest.q23, FoosTest.q24, FoosTest.q25, FoosTest.q26, FoosTest.q27,
    FoosTest.q28, FoosTest.q29, FoosTest.q30
]

TEST_PASS_SCORE = 23
MAX_POLL_QUESTION_LENGTH = 300

REDIS_ANSWER_PREFIX = 'answer_for_question'
REDIS_POLL_PREFIX = 'question_for_poll'
REDIS_ACTIVE_TEST_SESSION_KEY = 'active_test_session'


async def send_poll_from_question(
    chat_id: Union[int, str],
    user_id: Union[int, str],
    question: str,
    reply_markup: ReplyKeyboardMarkup
) -> Message:
    question_obj = questions[question]
    if not isinstance(question_obj, FoosTestQuestion):
        raise ValueError(f'Cant create poll for {question_obj} of type {type(question_obj)}')
    question_text = question_obj.text_with_enumeration
    message_part, poll_part = None, question_text
    if len(question_text) > MAX_POLL_QUESTION_LENGTH:
        question_text_parts = question_text.split('. ')
        message_part = '. '.join(question_text_parts[:-1]) + '.'
        poll_part = question_text_parts[-1]
        if len(poll_part) > MAX_POLL_QUESTION_LENGTH:
            logger.warning(f'Poll question {question_text} exceeds maximum poll length of {MAX_POLL_QUESTION_LENGTH}')
    if message_part:
        await dp.bot.send_message(
            chat_id=chat_id,
            text=message_part,
            reply_markup=reply_markup
        )
    poll_message = await dp.bot.send_poll(
        chat_id=chat_id,
        question=poll_part,
        options=question_obj.options,
        is_anonymous=False,
        type='regular',
        allows_multiple_answers=False,
        reply_markup=reply_markup
    )
    data = await dp.storage.get_data(user=user_id)
    data[f'{REDIS_POLL_PREFIX}{poll_message.poll.id}'] = question
    await dp.storage.update_data(user=user_id, data=data)
    return poll_message


async def send_open_question(
    chat_id: Union[int, str],
    question: str,
) -> Message:
    question_obj = questions[question]
    if not isinstance(question_obj, FoosTestOpenQuestion):
        raise ValueError(f'{question_obj} is not an open question, but {type(question_obj)}')
    return await dp.bot.send_message(
        chat_id=chat_id,
        text=question_obj.text_with_enumeration,
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message_handler(state='*', commands='start')
async def start_handler(message: Message) -> None:
    user = foos_test_service.get_user(message.from_user.id)
    if not user:
        logger.info(f'Got /start command from unknown user {message.from_user}')
        user = foos_test_service.create_user(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username
        )
    logger.info(f'Starting test session for user {user}')
    test_session = foos_test_service.create_test_session_for_user(user.user_id)
    logger.info(f'Started test session {test_session}')
    await dp.storage.reset_data(user=message.from_user.id)
    await dp.storage.update_data(user=message.from_user.id, data={
        REDIS_ACTIVE_TEST_SESSION_KEY: test_session.id
    })
    await FoosTest.q1.set()
    await message.answer(
        text=(
            'Тест состоит из трех секций по 10 вопросов. В первой секции требуется указать, истинно '
            'или ложно утверждение. Вторая секция состоит из вопросов с тремя вариантами ответа. В третьей секции '
            'вариантов ответа нет.\n'
            'Вопросы с вариантами ответа будут приходить в виде опросов. В каждом вопросе выберите один наиболее '
            'подходящий ответ. Для получения следующего вопроса нажмите на кнопку "следующий вопрос". Если клавиатура '
            'с кнопками скрыта, нажмите пиктограмму в виде четырех кнопок в правой части строки для ввода сообщения.\n'
            'В вопросах с вариантами ответа можно переголосовать сколько угодно раз. Для отмены голоса выберите и '
            'удерживайте палец на сообщении с опросом. В меню выберите пункт "отменить голос" и проголосуйте заново.\n'
            'Ответы на открытые вопросы (без вариантов ответа) присылайте обыкновенным сообщением. '
            'Изменить ответ на открытый вопрос нельзя.\n'
            'После ответа на последний вопрос все ваши ответы будут зафиксированы и смена голосов в опросах перестанет '
            'засчитываться.\n'
            'Если после ответа на последний вопрос некоторые вопросы останутся неотвеченными, вам будет предложено '
            'еще раз вернуться к ним.\n'
            'Если что-то пошло не по плану, отправьте команду "/start", и тестирование начнется заново.\n'
            'Желаю удачи! Нажмите "Начать тест" для старта тестирования.'
        ),
        reply_markup=start_keyboard
    )


def format_answers_for_test_session(test_session: TestSessionDto) -> str:
    answers = foos_test_service.get_test_session_answers(test_session.id)
    answers.sort(key=lambda ans: int(ans.question.code.replace('q', '')))

    def is_correct_to_emoji(is_correct: Optional[bool]) -> str:
        if is_correct is None:
            return emojize(':stopwatch:')
        elif is_correct:
            return emojize(':check_mark_button:')
        return emojize(':cross_mark:')

    res = f'На текущий момент ваш тест {"проверен" if test_session.is_checked else "не проверен"}.\n\n'
    res += '\n'.join([
        (
            f'Вопрос #{answer.question.code.replace("q", "")}: '
            f'{answer.answer} {is_correct_to_emoji(answer.is_correct)}'
        )
        for answer in answers
    ])
    if test_session.is_checked:
        test_passed = False
        if test_session.score >= TEST_PASS_SCORE:
            test_passed = True
        res += f'\n\nРезультат: {test_session.score} баллов. Успешная сдача от 23 баллов.'
        if test_passed:
            res += f'\nВы сдали! Поздравляю! {emojize(":party_popper:")}'
        else:
            res += '\nК сожалению, вам не хватило баллов для успешной сдачи теста. Попробуйте в следующий раз.'
    return res


@dp.message_handler(state=FoosTest.end)
async def end_handler(message: Message) -> None:
    data = await dp.storage.get_data(user=message.from_user.id)

    if message.text != END_TEST:
        # here we still got an answer for the last question
        last_question = get_last_question_code()
        data[f'{REDIS_ANSWER_PREFIX}{last_question}'] = message.text
        await dp.storage.update_data(user=message.from_user.id, data=data)

    answers = {}
    for key, value in data.items():
        if key.startswith(REDIS_ANSWER_PREFIX):
            answers[key.replace(REDIS_ANSWER_PREFIX, '')] = value

    user_answered_all_questions = len(answers.keys()) == TOTAL_QUESTIONS
    if not user_answered_all_questions:
        await message.answer(
            text='Вы ответили не на все вопросы. Проверьте свои голоса и нажмите "Завершить тест".',
            reply_markup=end_keyboard
        )
        return

    active_test_session_id = data[REDIS_ACTIVE_TEST_SESSION_KEY]
    test_session = foos_test_service.end_test_session(active_test_session_id, answers)
    results_text = format_answers_for_test_session(test_session)
    await FoosTest.next()
    await message.answer(
        f'Спасибо за тестирование! Ваши ответы сохранены.\n{results_text}', reply_markup=get_result_keyboard
    )


@dp.message_handler(state=FoosTest.results)
async def results_handler(message: Message) -> None:
    data = await dp.storage.get_data(user=message.from_user.id)
    active_test_session_id = data[REDIS_ACTIVE_TEST_SESSION_KEY]
    test_session = foos_test_service.get_test_session(active_test_session_id)
    results_text = format_answers_for_test_session(test_session)
    await message.answer(results_text, reply_markup=get_result_keyboard)


@dp.message_handler(Text(equals=[NEXT_QUESTION, START_TEST]), state=questions_with_options_states)
async def question_with_options_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    _, question = current_state.split(':')
    await FoosTest.next()
    await send_poll_from_question(
        chat_id=message.chat.id, user_id=message.from_user.id, question=question, reply_markup=question_keyboard
    )


@dp.message_handler(state=open_questions_states)
async def open_question_handler(message: Message, state: FSMContext) -> None:
    logger.info(message)
    current_state = await state.get_state()
    _, question = current_state.split(':')
    if message.text != NEXT_QUESTION:
        # here we always get answer for previous question
        previous_question = get_previous_question_code(question)
        data = await dp.storage.get_data(user=message.from_user.id)
        data[f'{REDIS_ANSWER_PREFIX}{previous_question}'] = message.text
        logger.info(f'open_question_handler: saved answer {message.text} for question {previous_question}')
        await dp.storage.update_data(user=message.from_user.id, data=data)
    await FoosTest.next()
    await send_open_question(chat_id=message.chat.id, question=question)


@dp.poll_answer_handler()
async def poll_handler(poll_answer: PollAnswer) -> None:
    logger.info(f'Got poll answer {poll_answer}')
    data = await dp.storage.get_data(user=poll_answer.user.id)
    question = data[f'{REDIS_POLL_PREFIX}{poll_answer.poll_id}']
    if poll_answer.option_ids:
        data[f'{REDIS_ANSWER_PREFIX}{question}'] = poll_answer.option_ids[0]
    else:  # vote retracted
        data.pop(f'{REDIS_ANSWER_PREFIX}{question}', None)
    await dp.storage.update_data(user=poll_answer.user.id, data=data)


if __name__ == '__main__':
    start_app()
