import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import Dispatcher
from aiogram.bot import Bot
from aiogram.utils.executor import start_webhook
from settings import (
    webhook_path, webhook_url, webapp_host, webapp_port, telegram_token, database_uri, log_level,
    redis_host, redis_port, redis_db
)


level = logging.getLevelName(log_level)
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)

bot = Bot(token=telegram_token)
storage = RedisStorage2(host=redis_host, port=redis_port, db=redis_db)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(_: Dispatcher) -> None:
    await bot.set_webhook(webhook_url)


async def on_shutdown(_: Dispatcher) -> None:
    await dp.storage.close()
    await dp.storage.wait_closed()
    await bot.delete_webhook(webhook_url)


def start_app() -> None:
    start_webhook(
        dispatcher=dp,
        webhook_path=webhook_path,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=webapp_host,
        port=webapp_port,
        skip_updates=True
    )
