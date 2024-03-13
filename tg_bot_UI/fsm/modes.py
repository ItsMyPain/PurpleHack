from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class Mode(StatesGroup):
    silent = State()
    detailed = State()