from aiogram import Bot, Router, F
from kbd import CallbackButtons, Keyboards
from aiogram.types import CallbackQuery, Message
import logging
from .states import AddHostAction
from aiogram.fsm.context import FSMContext
from utils.helpers import run_command

dp = Router()
log = logging.getLogger("hosts")


@dp.callback_query(F.data == CallbackButtons.host_manage.value)
async def manage_hosts_menu(cq: CallbackQuery, bot: Bot):
    msg = cq.message
    assert msg is not None
    await bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=msg.message_id,
        text="Управления хостами",
        reply_markup=Keyboards.host_manage_menu(),
    )


@dp.callback_query(F.data == CallbackButtons.add_host.value)
async def add_host(cq: CallbackQuery, bot: Bot, state: FSMContext):
    msg = cq.message
    assert msg is not None
    log.debug("User %s prompted to add host", msg.from_user.username)  # type: ignore
    await bot.send_message(
        msg.chat.id,
        "Введите домен(или несколько доменов, разделенных пробелом) для добавления:",
        # reply_markup=Keyboards.host_manage_menu(),
    )
    await state.set_state(AddHostAction.wait_host)


@dp.message(AddHostAction.wait_host)
async def get_host_for_adding(msg: Message, bot: Bot, state: FSMContext):
    assert msg.text is not None
    await state.clear()
    domain_list = msg.text.split()
    for domain in domain_list:
        msg = await bot.send_message(chat_id=msg.chat.id, text=f'Adding "{domain}" domain...')
        out = await run_command(f'kvas add "{domain}" yes')
        await bot.edit_message_text(
            chat_id=msg.chat.id, message_id=msg.message_id, text=f'Success added "{domain}" domain.\n {out}'
        )
