from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    username = State()
    place = State()
    day = State()
    time_start = State()
    duration = State()
    people_group = State()








