from aiogram.fsm.state import State, StatesGroup


class AddHostAction(StatesGroup):
    wait_host: State = State()


class DeleteHostAction(StatesGroup):
    wait_host: State = State()
