from aiogram.fsm.state import StatesGroup, State


class Reg(StatesGroup):
    place = State()
    time_start = State()
    time_end = State()
    group = State()








