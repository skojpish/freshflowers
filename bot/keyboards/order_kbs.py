from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Basket
def add_basket_kb() -> InlineKeyboardMarkup:
    """Get kb after adding item to the basket
    """
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Продолжить покупки", callback_data="continue"
    ))
    kb.add(InlineKeyboardButton(
        text="Перейти в корзину", callback_data="basket"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def basket_kb() -> InlineKeyboardMarkup:
    """Get basket kb
    """
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Оформить заказ", callback_data="reg_order"
    ))
    kb.add(InlineKeyboardButton(
        text="Изменить данные", callback_data="change_basket"
    ))
    kb.add(InlineKeyboardButton(
        text="Продолжить покупки", callback_data="continue"
    ))
    kb.add(InlineKeyboardButton(
        text="Очистить корзину", callback_data="delete_basket"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def basket_empty_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Продолжить покупки", callback_data="continue"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def otw_empty_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Товары в наличии", callback_data="in_stock"
    ))
    kb.add(InlineKeyboardButton(
        text="Оформить предзаказ", callback_data="pre_order"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def inst_empty_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Товары в пути", callback_data="on_the_way"
    ))
    kb.add(InlineKeyboardButton(
        text="Оформить предзаказ", callback_data="pre_order"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

# Order register
def business_type_kb() -> InlineKeyboardMarkup:
    """Get choice business kb
    """
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Частное лицо", callback_data="person"
    ))
    kb.add(InlineKeyboardButton(
        text="Магазин", callback_data="shop"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def preord_kb() -> InlineKeyboardMarkup:
    """Get pre-order kb
    """
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Оформить заказ", callback_data="reg_order"
    ))
    kb.add(InlineKeyboardButton(
        text="Добавить предзаказ в корзину", callback_data="add_preord_to_basket"
    ))
    kb.add(InlineKeyboardButton(
        text="Отредактировать данные", callback_data="edit_pre_order"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

# Continue shopping
def continue_kb() -> InlineKeyboardMarkup:
    """Get kb for continue shopping
    """
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Товары в пути", callback_data="on_the_way"
    ))
    kb.add(InlineKeyboardButton(
        text="Товары в наличии", callback_data="in_stock"
    ))
    kb.add(InlineKeyboardButton(
        text="Предзаказ", callback_data="pre_order"
    ))
    kb.add(InlineKeyboardButton(
        text="Перейти в корзину", callback_data="basket"
    ))
    kb.adjust(1)
    return kb.as_markup()

# Send order
def send_order_kb() -> InlineKeyboardMarkup:
    """Get order send kb
    """
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Отправить заявку", callback_data="send_order"
    ))
    kb.add(InlineKeyboardButton(
        text="Изменить данные", callback_data="change_order"
    ))
    kb.add(InlineKeyboardButton(
        text="Продолжить покупки", callback_data="continue"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()


