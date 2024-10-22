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

class addProfit(StatesGroup):
    user_id = State()
    profits_amount = State()

class RemoveUserForm(StatesGroup):
    user_id = State()
class msgEveryone(StatesGroup):
    message = State()