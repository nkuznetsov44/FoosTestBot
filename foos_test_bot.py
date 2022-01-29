import logging
from aiogram.types import Message
from app import dp, start_app


logger = logging.getLogger(__name__)


@dp.message_handler()
async def echo_handler(message: Message) -> None:
    await message.answer(message.text)


if __name__ == '__main__':
    start_app()
