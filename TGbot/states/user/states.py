from aiogram.dispatcher.fsm.state import State, StatesGroup

class StateExample(StatesGroup):
    value = State()

class Answer(StatesGroup):
    userId = State()
    text = State()

class registation(StatesGroup):
    code = State()

class changeReq(StatesGroup):
    value = State()
    wallet = State()