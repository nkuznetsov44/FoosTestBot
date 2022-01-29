from aiogram.dispatcher.filters.state import State, StatesGroup


class FoosTest(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    end = State()
