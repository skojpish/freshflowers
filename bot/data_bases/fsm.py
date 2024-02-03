from aiogram.fsm.state import StatesGroup, State

class OrderInfo(StatesGroup):
    count_otw = State()
    count_inst = State()
    count_buy_now_otw = State()
    count_buy_now_inst = State()

class OrderConfirm(StatesGroup):
    full_name = State()
    number = State()

class PreOrder(StatesGroup):
    desc = State()

class OrderEdit(StatesGroup):
    otw_count = State()
    inst_count = State()
    pre_ord = State()
    full_name = State()
    number = State()
