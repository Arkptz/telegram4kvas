from re import L
from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from config import SETTINGS
from routers.hosts import dp as hosts_router
import logging
from log import *  # noqa
from aiogram.types import Message
from kbd import Keyboards

log = logging.getLogger("main")
dp = Dispatcher()
dp.include_routers(
    hosts_router,
)
bot = Bot(SETTINGS.token)


@dp.startup.register
async def startup():
    log.info("Bot was started...")


@dp.message(CommandStart())
async def start(
    msg: Message,
    bot: Bot,
):
    await bot.send_message(
        chat_id=msg.chat.id,
        text="Главное меню",
        reply_markup=Keyboards.main_menu(),
    )


def main():
    dp.run_polling(bot)


if __name__ == "__main__":

    main()
