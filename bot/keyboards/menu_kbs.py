from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_kb() -> InlineKeyboardMarkup:
    """Get kb for start menu
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
        text="Прайс лист", callback_data="price_list"
    ))
    kb.add(InlineKeyboardButton(
        text="Как это работает", callback_data="about"
    ))
    kb.add(InlineKeyboardButton(
        text="Корзина", callback_data="basket"
    ))
    kb.add(InlineKeyboardButton(
        text="Наш канал", callback_data="channel"
    ))
    kb.adjust(1)
    return kb.as_markup()

# Scheduler kb
def scheduler_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Сделать заказ", callback_data="back_to_menu_photo"
    ))
    kb.adjust(1)
    return kb.as_markup()

def back_to_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def back_to_menu_photo_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu_photo"
    ))
    kb.adjust(1)
    return kb.as_markup()