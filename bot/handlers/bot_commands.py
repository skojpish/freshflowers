from aiogram.types import BotCommand, CallbackQuery

from bot.config import bot

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.data_bases.basket import db_basket

from bot.keyboards.menu_kbs import start_kb
from bot.keyboards.order_kbs import basket_kb, basket_empty_kb

router = Router()

# Get bot menu commands
async def setup_bot_commands():
    bot_commands = [
        BotCommand(command="/basket", description="Перейти в корзину"),
        BotCommand(command="/menu", description="Вернуться в главное меню")
    ]
    return await bot.set_my_commands(bot_commands)

# Get start menu
@router.message(Command("start"))
async def cmd_start(msg: Message) -> None:
    await db_basket.add_user_to_stat(msg.from_user.id, msg.from_user.username)
    await msg.answer(f"Привет, {msg.from_user.full_name}!\n"
                     f"В этом боте ты можешь заказать цветы", reply_markup=start_kb())


@router.message(Command("menu"))
async def cmd_back_to_menu(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await db_basket.delete_item_if_null(msg.from_user.id)
    await msg.answer(f"Привет, {msg.from_user.full_name}!\n"
                     f"В этом боте ты можешь заказать цветы", reply_markup=start_kb())

@router.callback_query(F.data == "back_to_menu")
async def menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await db_basket.delete_item_if_null(callback.from_user.id)
    await callback.message.edit_text(f"Привет, {callback.from_user.full_name}!\n"
                     f"В этом боте ты можешь заказать цветы")
    await callback.message.edit_reply_markup(reply_markup=start_kb())
    await callback.answer()

@router.callback_query(F.data == "back_to_menu_photo")
async def menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await db_basket.delete_item_if_null(callback.from_user.id)
    await callback.message.answer(f"Привет, {callback.from_user.full_name}!\n"
                     f"В этом боте ты можешь заказать цветы", reply_markup=start_kb())
    await callback.answer()

@router.callback_query(F.data == "back")
async def back(callback: CallbackQuery) -> None:
    await callback.message.delete()
    await callback.answer()

# Basket
@router.message(Command("basket"))
async def basket(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await db_basket.delete_item_if_null(msg.from_user.id)

    items_otw = []
    items_inst = []
    pre_ord = []
    items_otw_exist: bool = False
    items_inst_exist: bool = False
    pre_order_exist: bool = False

    basket_data = await db_basket.print_basket(msg.from_user.id)
    for item in basket_data:
        data = {
            'item': item[2],
            'col': item[3],
            'pre_ord': item[4],
            'category': item[5]
        }

        if data['item'] is not None and data['category'] == 'otw' and data['pre_ord'] is None:
            items_otw_exist = True
            items_otw.append(f"{data['item']}: {data['col']} шт")
        elif data['item'] is not None and data['category'] == 'inst' and data['pre_ord'] is None:
            items_inst_exist = True
            items_inst.append(f"{data['item']}: {data['col']} шт")
        else:
            pre_order_exist = True
            pre_ord.append(f"{data['pre_ord']}")

    new_line = '\n'

    if pre_order_exist and items_otw_exist and not items_inst_exist:
        await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                         f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                         f"<b>Предзаказ:</b>\n"
                                         f"{pre_ord[0]}", reply_markup=basket_kb())
    elif pre_order_exist and not items_otw_exist and not items_inst_exist:
        await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                         f"<b>Предзаказ:</b>\n"
                                         f"{pre_ord[0]}", reply_markup=basket_kb())
    elif not pre_order_exist and items_otw_exist and not items_inst_exist:
        await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                         f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}", reply_markup=basket_kb())
    elif pre_order_exist and not items_otw_exist and items_inst_exist:
        await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                         f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                         f"<b>Предзаказ:</b>\n"
                                         f"{pre_ord[0]}", reply_markup=basket_kb())
    elif not pre_order_exist and not items_otw_exist and items_inst_exist:
        await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                         f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}", reply_markup=basket_kb())
    elif pre_order_exist and items_otw_exist and items_inst_exist:
        await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                         f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                         f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                         f"<b>Предзаказ:</b>\n"
                                         f"{pre_ord[0]}", reply_markup=basket_kb())
    elif not pre_order_exist and items_otw_exist and items_inst_exist:
        await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                         f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                         f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}", reply_markup=basket_kb())
    else:
        await msg.answer(f"Корзина пуста", reply_markup=basket_empty_kb())



