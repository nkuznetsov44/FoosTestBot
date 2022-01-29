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


async def send_poll_from_question(
    chat_id: Union[int, str],
    user_id: Union[int, str],
    question: str,
    reply_markup: ReplyKeyboardMarkup
) -> Message:
    question_obj = get_question(question)
    poll_message = await dp.bot.send_poll(
        chat_id=chat_id,
        question=question_obj.question,
        options=question_obj.options,
        is_anonymous=False,
        type='regular',
        allows_multiple_answers=False,
        reply_markup=reply_markup
    )
    data = await dp.storage.get_data(user=user_id)
    data[f'question_for_poll{poll_message.poll.id}'] = question
    await dp.storage.update_data(user=user_id, data=data)
    return poll_message


@dp.message_handler(state='*', commands='start')
async def start_handler(message: Message) -> None:
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
    await send_poll_from_question(
        chat_id=message.chat.id, user_id=message.from_user.id, question=question, reply_markup=end_keyboard
    )


@dp.message_handler(Text(equals=[NEXT_QUESTION, START_TEST]), state='*')
async def question_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    _, question = current_state.split(':')
    await FoosTest.next()
    await send_poll_from_question(
        chat_id=message.chat.id, user_id=message.from_user.id, question=question, reply_markup=question_keyboard
    )


@dp.message_handler(Text(equals=END_TEST), state='*')
async def end_handler(message: Message, _: FSMContext) -> None:
    data = await dp.storage.get_data(user=message.from_user.id)
    answers = {}
    for key, value in data.items():
        if key.startswith('answer_for_question'):
            answers[key] = value
    user_answered_all_questions = True  # TODO
    if not user_answered_all_questions:
        await message.answer(
            text='Вы ответили не на все вопросы. Проверьте свои голоса и снова нажмите "Завершить тест".',
            reply_markup=end_keyboard
        )
    else:
        await message.answer(
            f'Спасибо за тестирование! Ваши ответы: {answers}', reply_markup=None
        )


@dp.poll_answer_handler()
async def poll_handler(poll_answer: PollAnswer) -> None:
    logger.info(poll_answer)
    data = await dp.storage.get_data(user=poll_answer.user.id)
    question = data[f'question_for_poll{poll_answer.poll_id}']
    if poll_answer.option_ids:
        data[f'answer_for_question{question}'] = poll_answer.option_ids[0]
    else:  # vote retracted
        data.pop(f'answer_for_question{question}', None)
    await dp.storage.update_data(user=poll_answer.user.id, data=data)


if __name__ == '__main__':
    start_app()
