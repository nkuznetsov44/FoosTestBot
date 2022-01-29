from typing import Union
import logging
from aiogram.types import Message, PollAnswer, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from app import dp, start_app
from foostest import FoosTest
from questions import get_question, TOTAL_QUESTIONS


logger = logging.getLogger(__name__)

START_TEST = 'Начать тест'
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(START_TEST))

NEXT_QUESTION = 'Следующий вопрос'
question_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(NEXT_QUESTION))

LAST_QUESTION_STATE = FoosTest.q3
END_TEST = 'Завершить тест'
end_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(END_TEST))


answers = {}
poll_to_question = {}


def all_questions_answered_by_user(user_id: Union[int, str]) -> bool:
    return len(answers[user_id].keys()) == TOTAL_QUESTIONS


async def send_poll_from_question(chat_id: Union[int, str], question: str, reply_markup: ReplyKeyboardMarkup) -> Message:
    question = get_question(question)
    return await dp.bot.send_poll(
        chat_id=chat_id,
        question=question.question,
        options=question.options,
        is_anonymous=False,
        type='regular',
        allows_multiple_answers=False,
        reply_markup=reply_markup
    )


@dp.message_handler(state='*', commands='start')
async def start_handler(message: Message) -> None:
    poll_to_question[message.from_user.id] = {}
    answers[message.from_user.id] = {}
    await FoosTest.q1.set()
    await message.answer(
        text=(
            'Нажмите "Начать тест" для старта тестирования. После этого вопросы теста будут приходить в виде '
            'опроса. В каждом вопросе выберите один наиболее подходящий ответ. После ответа нажмите на кнопку '
            '"следующий вопрос". В каждом опросе можно проголосовать сколько угодно раз. После последнего вопроса '
            'появится кнопка "завершить тест". После нажатия на нее все ответы зафиксируются и изменение голоса '
            'больше не будет учитываться.'
        ),
        reply_markup=start_keyboard
    )


@dp.message_handler(Text(equals=[NEXT_QUESTION]), state=LAST_QUESTION_STATE)
async def last_question_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    _, question = current_state.split(':')
    poll_message = await send_poll_from_question(message.chat.id, question=question, reply_markup=end_keyboard)
    poll_to_question[message.from_user.id][poll_message.poll.id] = question


@dp.message_handler(Text(equals=[NEXT_QUESTION, START_TEST]), state='*')
async def question_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    _, question = current_state.split(':')
    await FoosTest.next()
    poll_message = await send_poll_from_question(message.chat.id, question=question, reply_markup=question_keyboard)
    poll_to_question[message.from_user.id][poll_message.poll.id] = question


@dp.message_handler(Text(equals=END_TEST), state='*')
async def end_handler(message: Message, state: FSMContext) -> None:
    if not all_questions_answered_by_user(message.from_user.id):
        await message.answer(
            text='Вы ответили не на все вопросы. Проверьте свои голоса и снова нажмите "Завершить тест".',
            reply_markup=end_keyboard
        )
    else:
        await message.answer(
            f'Спасибо за тестирование! Ваши ответы зафиксированы: {answers[message.from_user.id]}', reply_markup=None
        )


@dp.poll_answer_handler()
async def poll_handler(poll_answer: PollAnswer) -> None:
    logger.info(poll_answer)
    logger.info(poll_to_question)
    question = poll_to_question[poll_answer.user.id][poll_answer.poll_id]
    answers[poll_answer.user.id][question] = poll_answer.option_ids


if __name__ == '__main__':
    start_app()
