from typing import Union
import logging
from aiogram.types import Message, PollAnswer, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from app import dp, start_app
from foostest import FoosTest
from questions import (
    questions, TOTAL_QUESTIONS, get_previous_question_code, get_last_question_code,
    FoosTestQuestion, FoosTestOpenQuestion
)


logger = logging.getLogger(__name__)

START_TEST = 'Начать тест'
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(START_TEST))

NEXT_QUESTION = 'Следующий вопрос'
question_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(NEXT_QUESTION))

END_TEST = 'Завершить тест'
end_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(END_TEST))

questions_with_options_states = [FoosTest.q1, FoosTest.q2, FoosTest.q3]
open_questions_states = [FoosTest.q4, FoosTest.q5]


async def send_poll_from_question(
    chat_id: Union[int, str],
    user_id: Union[int, str],
    question: str,
    reply_markup: ReplyKeyboardMarkup
) -> Message:
    question_obj = questions[question]
    if not isinstance(question_obj, FoosTestQuestion):
        raise ValueError(f'Cant create poll for {question_obj} of type {type(question_obj)}')
    poll_message = await dp.bot.send_poll(
        chat_id=chat_id,
        question=question_obj.text,
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


async def send_open_question(
    chat_id: Union[int, str],
    question: str,
) -> Message:
    question_obj = questions[question]
    if not isinstance(question_obj, FoosTestOpenQuestion):
        raise ValueError(f'{question_obj} is not an open question, but {type(question_obj)}')
    return await dp.bot.send_message(
        chat_id=chat_id,
        text=question_obj.text,
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message_handler(state='*', commands='start')
async def start_handler(message: Message) -> None:
    await dp.storage.reset_data(user=message.from_user.id)
    await FoosTest.q1.set()
    await message.answer(
        text=(
            'Нажмите "Начать тест" для старта тестирования. После этого вопросы теста с вариантами ответа '
            'будут приходить в виде опроса. В каждом вопросе выберите один наиболее подходящий ответ. '
            'После ответа нажмите на кнопку "следующий вопрос". В вопросах с вариантами ответа можно переголосовать '
            'сколько угодно раз.\n'
            'После вопросов с вариантами ответа будут открытые вопросы. Ответы на них просто пришлите сообщением. '
            'Изменить ответ на открытый вопрос нельзя.\n'
            'После ответа на последний вопрос все ваши ответы будут зафиксированы и смена голосов перестанет '
            'засчитываться.\n'
            'Если после ответа на последний вопрос некоторые вопросы останутся неотвеченными, вам будет предложено '
            'еще раз вернуться к ним.'
        ),
        reply_markup=start_keyboard
    )


@dp.message_handler(state=FoosTest.end)
async def end_handler(message: Message) -> None:
    data = await dp.storage.get_data(user=message.from_user.id)

    if message.text != END_TEST:
        # here we still got an answer for the last question
        last_question = get_last_question_code()
        data[f'answer_for_question{last_question}'] = message.text
        await dp.storage.update_data(user=message.from_user.id, data=data)

    answers = {}
    for key, value in data.items():
        if key.startswith('answer_for_question'):
            answers[key] = value
    user_answered_all_questions = len(answers.keys()) == TOTAL_QUESTIONS
    if not user_answered_all_questions:
        await message.answer(
            text='Вы ответили не на все вопросы. Проверьте свои голоса и нажмите "Завершить тест".',
            reply_markup=end_keyboard
        )
    else:
        await message.answer(
            f'Спасибо за тестирование! Ваши ответы: {answers}', reply_markup=None
        )


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
    current_state = await state.get_state()
    _, question = current_state.split(':')
    if message.text != NEXT_QUESTION:
        # here we always get answer for previous question
        previous_question = get_previous_question_code(question)
        data = await dp.storage.get_data(user=message.from_user.id)
        data[f'answer_for_question{previous_question}'] = message.text
        logger.info(f'open_question_handler: saved answer {message.text} for question {previous_question}')
        await dp.storage.update_data(user=message.from_user.id, data=data)
    await FoosTest.next()
    await send_open_question(chat_id=message.chat.id, question=question)


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
