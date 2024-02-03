from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def final_basket_edit_kb() -> InlineKeyboardMarkup:
    """Get kb after edit item from the basket
    """
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Перейти в корзину", callback_data="basket"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def final_order_edit_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Перейти к заявке", callback_data="reg_order"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def choise_edit_cat_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Данные о товарах", callback_data="change_basket_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Данные о себе", callback_data="change_about"
    ))
    kb.add(InlineKeyboardButton(
        text="Назад", callback_data="back"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def edit_about_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Тип бизнеса", callback_data="edit_type"
    ))
    kb.add(InlineKeyboardButton(
        text="ФИО", callback_data="edit_fname"
    ))
    kb.add(InlineKeyboardButton(
        text="Номер телефона", callback_data="edit_number"
    ))
    kb.add(InlineKeyboardButton(
        text="Назад", callback_data="back_edit_menu"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def edit_business_type_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Частное лицо", callback_data="edit_person"
    ))
    kb.add(InlineKeyboardButton(
        text="Магазин", callback_data="edit_shop"
    ))
    kb.add(InlineKeyboardButton(
        text="Назад", callback_data="change_about"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def edit_states_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Назад", callback_data="change_about"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()