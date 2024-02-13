from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.data_bases.basket import db_basket
from bot.data_bases.fsm import OrderEdit
from bot.data_bases.in_stock import db_inst
from bot.data_bases.order import db_ord
from bot.data_bases.psql_get import db_otw
from bot.keyboards.edit_kbs import final_basket_edit_kb, choise_edit_cat_kb, edit_about_kb, edit_business_type_kb, \
    final_order_edit_kb, edit_states_kb
from bot.keyboards.menu_kbs import back_to_menu_kb

router = Router()

# Change basket data
class BasketItemsCF(CallbackData, prefix="basket", sep="_"):
    basket_item_id: int
    changes: bool = False
    delete_item: bool = False
    change_count: bool = False
    change_preord: bool = False
    otw_items: bool = False
    inst_items: bool = False

@router.callback_query(F.data == "change_basket")
async def change_basket(callback: CallbackQuery) -> None:
    async def change_basket_kb() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        rows = await db_basket.print_basket(callback.from_user.id)

        otw_exist: bool = False
        inst_exist: bool = False
        pre_ord_exist: bool = False
        pre_ord_index = None

        for row in rows:
            cat = row[5]
            if cat == 'otw':
                otw_exist = True
            elif cat == 'inst':
                inst_exist = True
            elif cat is None:
                pre_ord_exist = True
                pre_ord_index = rows.index(row) + 1

        if otw_exist and inst_exist and not pre_ord_exist:
            kb.button(
                text="Товары в пути", callback_data="otw_edit"
            )
            kb.button(
                text="Товары в наличии", callback_data="inst_edit"
            )
        elif otw_exist and inst_exist and pre_ord_exist:
            kb.button(
                text="Товары в пути", callback_data="otw_edit"
            )
            kb.button(
                text="Товары в наличии", callback_data="inst_edit"
            )
            kb.button(
                text="Предзаказ", callback_data=BasketItemsCF(basket_item_id=f'{pre_ord_index}')
            )
        elif otw_exist != inst_exist:
            for row in rows:
                data = {
                    'item': row[2],
                    'col': row[3],
                    'pre_ord': row[4],
                    'cat': row[5]
                }
                if data['pre_ord'] is None:
                    kb.button(
                        text=f"{data['item']}", callback_data=BasketItemsCF(basket_item_id=f'{rows.index(row)+1}')
                    )
                elif data['pre_ord'] is not None:
                    kb.button(
                        text=f"Предзаказ", callback_data=BasketItemsCF(basket_item_id=f'{rows.index(row)+1}')
                    )
        kb.add(InlineKeyboardButton(
            text="Назад", callback_data="back"
        ))
        kb.adjust(1)
        return kb.as_markup()
    await callback.message.answer(f"Выберите категорию, которую вы хотели бы изменить", reply_markup=await change_basket_kb())
    await callback.answer()

@router.callback_query(F.data == "change_basket_edit")
async def change_basket(callback: CallbackQuery) -> None:
    async def change_basket_kb() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        rows = await db_basket.print_basket(callback.from_user.id)

        otw_exist: bool = False
        inst_exist: bool = False
        pre_ord_exist: bool = False
        pre_ord_index = None

        for row in rows:
            cat = row[5]
            if cat == 'otw':
                otw_exist = True
            elif cat == 'inst':
                inst_exist = True
            elif cat is None:
                pre_ord_exist = True
                pre_ord_index = rows.index(row) + 1

        if otw_exist and inst_exist and not pre_ord_exist:
            kb.button(
                text="Товары в пути", callback_data="otw_edit"
            )
            kb.button(
                text="Товары в наличии", callback_data="inst_edit"
            )
        elif otw_exist and inst_exist and pre_ord_exist:
            kb.button(
                text="Товары в пути", callback_data="otw_edit"
            )
            kb.button(
                text="Товары в наличии", callback_data="inst_edit"
            )
            kb.button(
                text="Предзаказ", callback_data=BasketItemsCF(basket_item_id=f'{pre_ord_index}')
            )
        elif otw_exist != inst_exist:
            for row in rows:
                data = {
                    'item': row[2],
                    'col': row[3],
                    'pre_ord': row[4],
                    'cat': row[5]
                }
                if data['pre_ord'] is None:
                    kb.button(
                        text=f"{data['item']}", callback_data=BasketItemsCF(basket_item_id=f'{rows.index(row)+1}')
                    )
                elif data['pre_ord'] is not None:
                    kb.button(
                        text=f"Предзаказ", callback_data=BasketItemsCF(basket_item_id=f'{rows.index(row)+1}')
                    )
        kb.add(InlineKeyboardButton(
            text="Назад", callback_data="back"
        ))
        kb.adjust(1)
        return kb.as_markup()
    await callback.message.edit_text(f"Выберите категорию, которую вы хотели бы изменить")
    await callback.message.edit_reply_markup(reply_markup=await change_basket_kb())
    await callback.answer()

@router.callback_query(F.data == "otw_edit")
async def change_otw_items(callback: CallbackQuery) -> None:
    async def change_otw_items_kb() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        rows = await db_basket.print_basket(callback.from_user.id)

        for row in rows:
            data = {
                'otw_item': row[2],
                'otw_col': row[3],
                'pre_ord': row[4],
                'cat': row[5]
            }
            if data['cat'] == 'otw':
                kb.button(
                    text=f"{data['otw_item']}", callback_data=BasketItemsCF(basket_item_id=f'{rows.index(row)+1}')
                )
        kb.add(InlineKeyboardButton(
            text="Назад", callback_data="change_basket_edit"
        ))
        kb.adjust(1)
        return kb.as_markup()

    await callback.message.edit_text(f"Выберите позицию, которую вы хотели бы изменить")
    await callback.message.edit_reply_markup(reply_markup=await change_otw_items_kb())
    await callback.answer()

@router.callback_query(F.data == "inst_edit")
async def change_inst_items(callback: CallbackQuery) -> None:
    async def change_inst_items_kb() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        rows = await db_basket.print_basket(callback.from_user.id)

        for row in rows:
            data = {
                'inst_item': row[2],
                'inst_col': row[3],
                'pre_ord': row[4],
                'cat': row[5]
            }
            if data['cat'] == 'inst':
                kb.button(
                    text=f"{data['inst_item']}", callback_data=BasketItemsCF(basket_item_id=f'{rows.index(row)+1}')
                )
        kb.add(InlineKeyboardButton(
            text="Назад", callback_data="change_basket_edit"
        ))
        kb.adjust(1)
        return kb.as_markup()

    await callback.message.edit_text(f"Выберите позицию, которую вы хотели бы изменить")
    await callback.message.edit_reply_markup(reply_markup=await change_inst_items_kb())
    await callback.answer()

@router.callback_query(BasketItemsCF.filter(F.changes==False))
async def basket_items_callbacks(callback: CallbackQuery, callback_data: BasketItemsCF) -> None:
    row = await db_basket.get_specific_basket_row(callback.from_user.id, callback_data.basket_item_id)
    data = {
        'otw_item': row[2],
        'otw_col': row[3],
        'pre_ord': row[4],
        'cat': row[5]
    }
    if data['pre_ord'] is None:
        def change_basket_item_kb() -> InlineKeyboardMarkup:
            kb = InlineKeyboardBuilder()
            kb.button(
                text="Изменить количество", callback_data=BasketItemsCF(basket_item_id=f'{callback_data.basket_item_id}',
                                                                        changes=True, change_count=True)
            )
            kb.button(
                text="Удалить позицию", callback_data=BasketItemsCF(basket_item_id=f'{callback_data.basket_item_id}',
                                                                    changes=True, delete_item=True)
            )
            kb.add(InlineKeyboardButton(
                text="Назад", callback_data="back"
            ))
            kb.adjust(1)
            return kb.as_markup()

        await callback.message.edit_text(f"<b>Выбранная позиция</b>\n"
                                      f"{data['otw_item']}: {data['otw_col']} шт\n\n"
                                      f"Выберите что вы хотели бы изменить")
        await callback.message.edit_reply_markup(reply_markup=change_basket_item_kb())
    elif data['pre_ord'] is not None:
        def change_basket_item_kb() -> InlineKeyboardMarkup:
            kb = InlineKeyboardBuilder()
            kb.button(
                text="Изменить предзаказ", callback_data=BasketItemsCF(basket_item_id=f'{callback_data.basket_item_id}',
                                                                       changes=True, change_preord=True)
            )
            kb.button(
                text="Удалить позицию", callback_data=BasketItemsCF(basket_item_id=f'{callback_data.basket_item_id}',
                                                                    changes=True, delete_item=True)
            )
            kb.add(InlineKeyboardButton(
                text="Назад", callback_data="back"
            ))
            kb.adjust(1)
            return kb.as_markup()

        await callback.message.edit_text(f"<b>Ваш предзаказ:</b>\n"
                                      f"{data['pre_ord']}\n\n"
                                      f"Выберите что вы хотели бы изменить")
        await callback.message.edit_reply_markup(reply_markup=change_basket_item_kb())
    await callback.answer()

@router.callback_query(BasketItemsCF.filter(F.changes==True))
async def basket_items_callbacks(callback: CallbackQuery, callback_data: BasketItemsCF, state: FSMContext) -> None:
    if callback_data.change_count:
        row = await db_basket.get_specific_basket_row(callback.from_user.id, callback_data.basket_item_id)
        name = row[2]
        cat = row[5]

        if cat == 'otw':
            await db_basket.set_count_null(name, callback.from_user.id)
            await state.set_state(OrderEdit.otw_count)
        elif cat == 'inst':
            await db_basket.set_count_null(name, callback.from_user.id)
            await state.set_state(OrderEdit.inst_count)

        await callback.message.edit_text(f"Напишите количество, которое вы хотели бы заказать")
        await callback.message.edit_reply_markup(reply_markup=back_to_menu_kb())
    elif callback_data.delete_item:
        row = await db_basket.get_specific_basket_row(callback.from_user.id, callback_data.basket_item_id)
        if row[2] is not None:
            await db_basket.delete_item(row[2], callback.from_user.id)
        else:
            await db_basket.delete_pre_ord(callback.from_user.id)

        reg_info = await db_ord.get_ord_row(callback.from_user.id)
        if reg_info is None:
            await callback.message.edit_text(f"Позиция успешно удалена из корзины!")
            await callback.message.edit_reply_markup(reply_markup=final_basket_edit_kb())
        else:
            await callback.message.edit_text(f"Позиция успешно удалена из корзины!")
            await callback.message.edit_reply_markup(reply_markup=final_order_edit_kb())
    elif callback_data.change_preord:
        await state.set_state(OrderEdit.pre_ord)
        await callback.message.edit_text(f"Опишите в свободной форме ваш заказ в ОДНОМ сообщении")
        await callback.message.edit_reply_markup(reply_markup=back_to_menu_kb())
    await callback.answer()


# Edit basket states
@router.message(OrderEdit.pre_ord)
async def edit_pre_order_desc(msg: Message, state: FSMContext) -> None:
    await db_basket.update_pre_order(msg.text, msg.from_user.id)
    await state.clear()
    reg_info = await db_ord.get_ord_row(msg.from_user.id)
    if reg_info is None:
        await msg.answer(f"Данные успешно изменены!", reply_markup=final_basket_edit_kb())
    else:
        await msg.answer(f"Данные успешно изменены!", reply_markup=final_order_edit_kb())

@router.message(OrderEdit.otw_count)
async def edit_item_count(msg: Message, state: FSMContext) -> None:
    name = await db_basket.get_name_item_where_null(msg.from_user.id)
    row = await db_otw.get_row_by_name(name)
    count = row[6]
    mult = row[7]
    min = row[8]

    if min is not None and mult is None:
        if (int(msg.text) <= count and int(msg.text) >= min) or (count <= min and int(msg.text) > 0 and int(msg.text) <= count):
            await db_basket.add_items_count(int(msg.text), msg.from_user.id)
            await state.clear()
            reg_info = await db_ord.get_ord_row(msg.from_user.id)
            if reg_info is None:
                await msg.answer(f"Данные успешно изменены!", reply_markup=final_basket_edit_kb())
            else:
                await msg.answer(f"Данные успешно изменены!", reply_markup=final_order_edit_kb())
        elif int(msg.text) < min and int(msg.text) >= 0:
            await state.set_state(OrderEdit.otw_count)
            await msg.answer(f"<b>Вы ввели количество, меньшее, чем необходимый минимум!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        elif int(msg.text) < 0:
            await state.set_state(OrderEdit.otw_count)
            await msg.answer(f"<b>Вы ввели отрицательное количество!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        else:
            await state.set_state(OrderEdit.otw_count)
            await msg.answer(f"<b>Вы ввели количество, большее того, что есть в наличии!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
    elif mult is not None and min is None:
        if (int(msg.text) % mult == 0 and int(msg.text) <= count and int(msg.text) > 0) or (count <= mult and int(msg.text) > 0 and int(msg.text) <= count):
            await db_basket.add_items_count(int(msg.text), msg.from_user.id)
            await state.clear()
            reg_info = await db_ord.get_ord_row(msg.from_user.id)
            if reg_info is None:
                await msg.answer(f"Данные успешно изменены!", reply_markup=final_basket_edit_kb())
            else:
                await msg.answer(f"Данные успешно изменены!", reply_markup=final_order_edit_kb())
        elif int(msg.text) < 0:
            await state.set_state(OrderEdit.otw_count)
            await msg.answer(f"<b>Вы ввели отрицательное количество!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        elif int(msg.text) > count:
            await state.set_state(OrderEdit.otw_count)
            await msg.answer(f"<b>Вы ввели количество, большее того, что есть в наличии!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        else:
            await state.set_state(OrderEdit.otw_count)
            await msg.answer(f"<b>Вы ввели количество, которое не кратно, описанной выше кратности!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
    elif min is not None and mult is not None:
        if int(msg.text) <= count and int(msg.text) >= min and int(msg.text)%mult == 0:
            await db_basket.add_items_count(int(msg.text), msg.from_user.id)
            await state.clear()
            reg_info = await db_ord.get_ord_row(msg.from_user.id)
            if reg_info is None:
                await msg.answer(f"Данные успешно изменены!", reply_markup=final_basket_edit_kb())
            else:
                await msg.answer(f"Данные успешно изменены!", reply_markup=final_order_edit_kb())
        elif int(msg.text) < 0:
            await state.set_state(OrderEdit.otw_count)
            await msg.answer(f"<b>Вы ввели отрицательное количество!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        elif int(msg.text) > count:
            await state.set_state(OrderEdit.otw_count)
            await msg.answer(f"<b>Вы ввели количество, большее того, что есть в наличии!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                                          reply_markup=back_to_menu_kb())
        elif int(msg.text)%mult != 0:
            await state.set_state(OrderEdit.otw_count)
            await msg.answer(f"<b>Вы ввели количество, которое не кратно, описанной выше кратности!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        elif int(msg.text) < min and int(msg.text) >= 0:
            await state.set_state(OrderEdit.otw_count)
            await msg.answer(f"<b>Вы ввели количество, меньшее, чем необходимый минимум!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        else:
            await state.set_state(OrderEdit.otw_count)
            await msg.answer(f"<b>Вы ввели количество, большее того, что есть в наличии!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                                          reply_markup=back_to_menu_kb())

@router.message(OrderEdit.inst_count)
async def edit_item_count(msg: Message, state: FSMContext) -> None:
    name = await db_basket.get_name_item_where_null(msg.from_user.id)
    row = await db_inst.get_row_by_name(name)
    count = row[6]
    mult = row[7]
    min = row[8]

    if min is not None and mult is None:
        if (int(msg.text) <= count and int(msg.text) >= min) or (count <= min and int(msg.text) > 0 and int(msg.text) <= count):
            await db_basket.add_items_count(int(msg.text), msg.from_user.id)
            await state.clear()
            reg_info = await db_ord.get_ord_row(msg.from_user.id)
            if reg_info is None:
                await msg.answer(f"Данные успешно изменены!", reply_markup=final_basket_edit_kb())
            else:
                await msg.answer(f"Данные успешно изменены!", reply_markup=final_order_edit_kb())
        elif int(msg.text) < min and int(msg.text) >= 0:
            await state.set_state(OrderEdit.inst_count)
            await msg.answer(f"<b>Вы ввели количество, меньшее, чем необходимый минимум!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        elif int(msg.text) < 0:
            await state.set_state(OrderEdit.inst_count)
            await msg.answer(f"<b>Вы ввели отрицательное количество!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        else:
            await state.set_state(OrderEdit.inst_count)
            await msg.answer(f"<b>Вы ввели количество, большее того, что есть в наличии!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
    elif mult is not None and min is None:
        if (int(msg.text) % mult == 0 and int(msg.text) <= count and int(msg.text) > 0) or (count <= mult and int(msg.text) > 0 and int(msg.text) <= count):
            await db_basket.add_items_count(int(msg.text), msg.from_user.id)
            await state.clear()
            reg_info = await db_ord.get_ord_row(msg.from_user.id)
            if reg_info is None:
                await msg.answer(f"Данные успешно изменены!", reply_markup=final_basket_edit_kb())
            else:
                await msg.answer(f"Данные успешно изменены!", reply_markup=final_order_edit_kb())
        elif int(msg.text) < 0:
            await state.set_state(OrderEdit.inst_count)
            await msg.answer(f"<b>Вы ввели отрицательное количество!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        elif int(msg.text) > count:
            await state.set_state(OrderEdit.inst_count)
            await msg.answer(f"<b>Вы ввели количество, большее того, что есть в наличии!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        else:
            await state.set_state(OrderEdit.inst_count)
            await msg.answer(f"<b>Вы ввели количество, которое не кратно, описанной выше кратности!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
    elif min is not None and mult is not None:
        if (int(msg.text) <= count and int(msg.text) >= min and int(msg.text)%mult == 0) or (count < min and int(msg.text) <= count and int(msg.text) > 0):
            await db_basket.add_items_count(int(msg.text), msg.from_user.id)
            await state.clear()
            reg_info = await db_ord.get_ord_row(msg.from_user.id)
            if reg_info is None:
                await msg.answer(f"Данные успешно изменены!", reply_markup=final_basket_edit_kb())
            else:
                await msg.answer(f"Данные успешно изменены!", reply_markup=final_order_edit_kb())
        elif int(msg.text) < 0:
            await state.set_state(OrderEdit.inst_count)
            await msg.answer(f"<b>Вы ввели отрицательное количество!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        elif int(msg.text) > count:
            await state.set_state(OrderEdit.inst_count)
            await msg.answer(f"<b>Вы ввели количество, большее того, что есть в наличии!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                                          reply_markup=back_to_menu_kb())
        elif int(msg.text)%mult != 0:
            await state.set_state(OrderEdit.inst_count)
            await msg.answer(f"<b>Вы ввели количество, которое не кратно, описанной выше кратности!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        elif int(msg.text) < min and int(msg.text) >= 0:
            await state.set_state(OrderEdit.inst_count)
            await msg.answer(f"<b>Вы ввели количество, меньшее, чем необходимый минимум!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        else:
            await state.set_state(OrderEdit.inst_count)
            await msg.answer(f"<b>Вы ввели количество, большее того, что есть в наличии!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                                          reply_markup=back_to_menu_kb())

# Change order data
@router.callback_query(F.data == "change_order")
async def change_order(callback: CallbackQuery) -> None:
    await callback.message.answer("Какие параметры вы хотели бы изменить?", reply_markup=choise_edit_cat_kb())
    await callback.answer()

@router.callback_query(F.data == "change_about")
async def change_about(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Какой параметр вы хотели бы изменить?")
    await callback.message.edit_reply_markup(reply_markup=edit_about_kb())
    await callback.answer()

@router.callback_query(F.data == "back_edit_menu")
async def change_order(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Какие параметры вы хотели бы изменить?")
    await callback.message.edit_reply_markup(reply_markup=choise_edit_cat_kb())
    await callback.answer()

# Edit order data about
@router.callback_query(F.data == "edit_type")
async def change_order(callback: CallbackQuery) -> None:
    await callback.message.edit_text(f"Выберите тип вашего бизнеса")
    await callback.message.edit_reply_markup(reply_markup=edit_business_type_kb())
    await callback.answer()

@router.callback_query(F.data == "edit_person")
async def type_person(callback: CallbackQuery) -> None:
    await db_ord.add_bus_type(callback.from_user.id, 'Частное лицо')
    await callback.message.edit_text(f"Данные успешно изменены!")
    await callback.message.edit_reply_markup(reply_markup=final_order_edit_kb())
    await callback.answer()

@router.callback_query(F.data == "edit_shop")
async def type_shop(callback: CallbackQuery) -> None:
    await db_ord.add_bus_type(callback.from_user.id, 'Магазин')
    await callback.message.edit_text(f"Данные успешно изменены!")
    await callback.message.edit_reply_markup(reply_markup=final_order_edit_kb())
    await callback.answer()

@router.callback_query(F.data == "edit_fname")
async def change_f_name(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(OrderEdit.full_name)
    await callback.message.edit_text(f"Напишите ваши фамилию, имя и отчество")
    await callback.message.edit_reply_markup(reply_markup=edit_states_kb())
    await callback.answer()

@router.callback_query(F.data == "edit_number")
async def change_f_name(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(OrderEdit.number)
    await callback.message.edit_text(f"Напишите ваш номер телефона")
    await callback.message.edit_reply_markup(reply_markup=edit_states_kb())
    await callback.answer()

# Edit about states
@router.message(OrderEdit.full_name)
async def order_f_name(msg: Message, state: FSMContext) -> None:
    await db_ord.add_full_name(msg.from_user.id, msg.text)
    await state.clear()
    await msg.answer(f"Данные успешно изменены!", reply_markup=final_order_edit_kb())

@router.message(OrderEdit.number)
async def order_number(msg: Message, state: FSMContext) -> None:
    await db_ord.add_number(msg.from_user.id, msg.text)
    await state.clear()
    await msg.answer(f"Данные успешно изменены!", reply_markup=final_order_edit_kb())

