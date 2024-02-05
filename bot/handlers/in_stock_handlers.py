from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, CallbackQuery, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup, \
    Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.data_bases.basket import db_basket
from bot.data_bases.fsm import OrderInfo
from bot.data_bases.order import db_ord
from bot.data_bases.in_stock import db_inst
from bot.keyboards.menu_kbs import back_to_menu_kb
from bot.keyboards.order_kbs import add_basket_kb, business_type_kb, send_order_kb, inst_empty_kb

router = Router()

class CategoriesISCF(CallbackData, prefix='inst'):
    category: str
    starting_point: int = 0
    next_ten: bool = False

class ItemsISCF(CallbackData, prefix="iteminst", sep="_"):
    item_id: int = 0
    category: str

class AddItemsISCF(CallbackData, prefix="addinst", sep="_"):
    item_add_id: int = 0
    category: str
    buy_now: bool = False

# Categories
@router.callback_query(F.data == "in_stock")
async def in_stock_start(callback: CallbackQuery) -> None:
    categories = await db_inst.get_categories()

    if not categories:
        await callback.message.edit_text("Товаров в наличии пока что нет, но вы можете посмотреть товары в пути или "
                                         "оформить предзаказ ниже")
        await callback.message.edit_reply_markup(reply_markup=inst_empty_kb())
    else:
        def categories_kb() -> InlineKeyboardMarkup:
            kb = InlineKeyboardBuilder()
            for category in categories:
                kb.button(
                    text=f"{category}", callback_data=CategoriesISCF(category=f'{category}')
                )
            kb.add(InlineKeyboardButton(
                text=f"Вернуться в главное меню", callback_data="back_to_menu"
            ))
            kb.adjust(1)
            return kb.as_markup()
        await callback.message.edit_text("<b>Товары в наличии</b>\n\n"
                                         "Выберите раздел")
        await callback.message.edit_reply_markup(reply_markup=categories_kb())
    await callback.answer()

@router.callback_query(F.data == "other_cat_inst")
async def other_categories(callback: CallbackQuery) -> None:
    categories = await db_inst.get_categories()

    def categories_kb() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for category in categories:
            kb.button(
                text=f"{category}", callback_data=CategoriesISCF(category=f'{category}')
            )
        kb.add(InlineKeyboardButton(
            text=f"Вернуться в главное меню", callback_data="back_to_menu"
        ))
        kb.adjust(1)
        return kb.as_markup()

    await callback.message.answer("<b>Товары в наличии</b>\n\n"
                                  "Выберите раздел", reply_markup=categories_kb())
    await callback.answer()

# Get items from stock
@router.callback_query(CategoriesISCF.filter(F.next_ten==False))
async def categories_callbacks(callback: CallbackQuery, callback_data: CategoriesISCF) -> None:
    await callback.message.delete()

    items10 = []
    items_id = []
    items_name = []
    items_next = False

    data = await db_inst.get_category_data10(callback_data.category)

    for row in data:
        item_id = row[0]
        name = row[1]
        photo = row[2]
        image_id = row[10]
        name_image_id = row[11]

        if image_id is None or name_image_id != photo:
            if photo == '' and image_id is not None:
                items10.append(InputMediaPhoto(type='photo', media=f'{image_id}'))
                items_id.append(item_id)
            else:
                items10.append(InputMediaPhoto(type='photo', media=FSInputFile(f"django_admin/proj/media/{photo}")))
                items_id.append(item_id)
        elif image_id is not None and name_image_id == photo:
            items10.append(InputMediaPhoto(type='photo', media=f'{image_id}'))
            items_id.append(item_id)

        items_name.append(name)

    if len(items10) > 9:
        items_next = True

    def kb_build10() -> InlineKeyboardMarkup:
        kb10 = InlineKeyboardBuilder()
        for i in range(len(items10)):
            kb10.button(
                text=f"{i + 1}", callback_data=ItemsISCF(item_id=items_id[i], category=callback_data.category)
            )
        if items_next:
            kb10.button(
                text=f"Посмотреть еще", callback_data=CategoriesISCF(starting_point=10, next_ten=True,
                                                                   category=callback_data.category)
            )
        kb10.add(InlineKeyboardButton(
            text="Посмотреть другие разделы", callback_data="other_cat_inst"
        ))
        kb10.add(InlineKeyboardButton(
            text="Вернуться в главное меню", callback_data="back_to_menu_photo"
        ))
        if len(items10) > 5:
            kb10.adjust(5, len(items10) - 5, 1, 1, 1)
        else:
            kb10.adjust(len(items10), 1, 1)
        return kb10.as_markup()

    media_gr = await callback.message.answer_media_group(items10)

    for row in data:
        item_id = row[0]
        photo = row[2]
        image_id = row[10]
        name_image_id = row[11]

        if image_id is None or photo != name_image_id:
            image_id_cur = media_gr[data.index(row)].photo[-1].file_id
            await db_inst.add_image_id(item_id, image_id_cur, photo)
        else:
            pass

    new_line = '\n'

    await callback.message.answer(f"Раздел: {callback_data.category}\n\n"
                                  f"{new_line.join([f'{items_name.index(name) + 1}. ' + str(name) for name in items_name])}\n\n"
                                  f"Выберите номер понравившейся позиции",
                                  reply_markup=kb_build10())
    await callback.answer()

# More than 10
@router.callback_query(CategoriesISCF.filter(F.next_ten==True))
async def in_stock20(callback: CallbackQuery, callback_data: CategoriesISCF) -> None:
    items20 = []
    items_id = []
    items_name = []
    items_next = False

    data = await db_inst.get_category_data_more(callback_data.category, callback_data.starting_point)

    for row in data:
        item_id = row[0]
        name = row[1]
        photo = row[2]
        image_id = row[10]
        name_image_id = row[11]

        if image_id is None or name_image_id != photo:
            if photo == '' and image_id is not None:
                items20.append(InputMediaPhoto(type='photo', media=f'{image_id}'))
                items_id.append(item_id)
            else:
                items20.append(InputMediaPhoto(type='photo', media=FSInputFile(f"django_admin/proj/media/{photo}")))
                items_id.append(item_id)
        elif image_id is not None and name_image_id == photo:
            items20.append(InputMediaPhoto(type='photo', media=f'{image_id}'))
            items_id.append(item_id)

        items_name.append(name)

    if len(items20) > 9:
        items_next = True

    def kb_build20() -> InlineKeyboardMarkup:
        kb20 = InlineKeyboardBuilder()
        for i in range(len(items20)):
            kb20.button(
                text=f"{i+1+callback_data.starting_point}", callback_data=ItemsISCF(item_id=items_id[i], category=callback_data.category)
            )
        if items_next:
            kb20.button(
                text="Посмотреть еще", callback_data=CategoriesISCF(starting_point=callback_data.starting_point + 10,
                                                                  next_ten=True, category=callback_data.category)
            )
        kb20.add(InlineKeyboardButton(
            text="Посмотреть другие разделы", callback_data="other_cat_inst"
        ))
        kb20.add(InlineKeyboardButton(
            text="Вернуться в главное меню", callback_data="back_to_menu_photo"
        ))
        if len(items20) > 5:
            kb20.adjust(5, len(items20)-5, 1, 1)
        else:
            kb20.adjust(len(items20), 1, 1)
        return kb20.as_markup()

    media_gr = await callback.message.answer_media_group(items20)

    for row in data:
        item_id = row[0]
        photo = row[2]
        image_id = row[10]
        name_image_id = row[11]

        if image_id is None or photo != name_image_id:
            image_id_cur = media_gr[data.index(row)].photo[-1].file_id
            await db_inst.add_image_id(item_id, image_id_cur, photo)
        else:
            pass

    new_line = '\n'

    await callback.message.answer(f"Раздел: {callback_data.category}\n\n"
                                  f"{new_line.join([f'{items_name.index(name)+1+callback_data.starting_point}. '+str(name) for name in items_name])}\n\n"
                                  f"Выберите номер понравившейся позиции", reply_markup=kb_build20())
    await callback.answer()

# Item
@router.callback_query(ItemsISCF.filter())
async def in_stock_callbacks(callback: CallbackQuery, callback_data: ItemsISCF) -> None:
    row = await db_inst.get_specific_row(callback_data.item_id)
    data = {
        'name': row[1],
        'descrip': row[3],
        'price': row[5],
        'col': row[6],
        'mult': row[7],
        'min': row[8],
        'date': row[9],
        'photo': row[10]
    }

    def items_order_kb() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.button(
            text="Купить сейчас",
            callback_data=AddItemsISCF(item_add_id=f'{callback_data.item_id}', category=callback_data.category, buy_now=True)
        )
        kb.button(
            text="Добавить в корзину", callback_data=AddItemsISCF(item_add_id=f'{callback_data.item_id}', category=callback_data.category)
        )
        kb.add(InlineKeyboardButton(
            text="Назад", callback_data="back"
        ))
        kb.add(InlineKeyboardButton(
            text="Вернуться в главное меню", callback_data="back_to_menu_photo"
        ))
        kb.adjust(1)
        return kb.as_markup()
    if data['mult'] is not None and data['min'] is None:
        if data['col'] > data['mult']:
            await callback.message.answer_photo(data['photo'], f"{data['name']}\n"
                                                               f"{data['descrip']}\n"
                                                               f"Цена: {data['price']} руб\n"
                                                               f"Оставшееся количество: {data['col']} шт\n"
                                                               f"Кратность: {data['mult']}*\n"
                                                               f"Прибыл: {data['date'].strftime('%d.%m.%Y')}\n\n"
                                                               f"* можно заказать лишь КРАТНОЕ данному числу количество",
                                                               reply_markup=items_order_kb())
        elif data['col'] <= data['mult']:
            await callback.message.answer_photo(data['photo'], f"{data['name']}\n"
                                                               f"{data['descrip']}\n"
                                                               f"Цена: {data['price']} руб\n"
                                                               f"Оставшееся количество: {data['col']} шт\n"
                                                               f"Прибыл: {data['date'].strftime('%d.%m.%Y')}",
                                                               reply_markup=items_order_kb())
    elif data['min'] is not None and data['mult'] is None:
        if data['col'] > data['min']:
            await callback.message.answer_photo(data['photo'], f"{data['name']}\n"
                                                               f"{data['descrip']}\n"
                                                               f"Цена: {data['price']} руб\n"
                                                               f"Оставшееся количество: {data['col']} шт\n"
                                                               f"Минимальный заказ: {data['min']}*\n"
                                                               f"Прибыл: {data['date'].strftime('%d.%m.%Y')}\n\n"
                                                               f"* можно заказать лишь НЕ МЕНЬШЕ данного числа количество",
                                                               reply_markup=items_order_kb())
        elif data['col'] <= data['min']:
            await callback.message.answer_photo(data['photo'], f"{data['name']}\n"
                                                               f"{data['descrip']}\n"
                                                               f"Цена: {data['price']} руб\n"
                                                               f"Оставшееся количество: {data['col']} шт\n"
                                                               f"Прибыл: {data['date'].strftime('%d.%m.%Y')}",
                                                               reply_markup=items_order_kb())
    else:
        if data['col'] > data['min']:
            await callback.message.answer_photo(data['photo'], f"{data['name']}\n"
                                                               f"{data['descrip']}\n"
                                                               f"Цена: {data['price']} руб\n"
                                                               f"Оставшееся количество: {data['col']} шт\n"
                                                               f"Минимальный заказ: {data['min']}*\n"
                                                               f"Кратность: {data['mult']}**\n"
                                                               f"Дата прибытия: {data['date'].strftime('%d.%m.%Y')}\n\n"
                                                               f"* можно заказать лишь НЕ МЕНЬШЕ данного числа количество\n"
                                                               f"** можно заказать лишь КРАТНОЕ данному числу количество",
                                                reply_markup=items_order_kb())
        elif data['col'] <= data['min']:
            await callback.message.answer_photo(data['photo'], f"{data['name']}\n"
                                                               f"{data['descrip']}\n"
                                                               f"Цена: {data['price']} руб\n"
                                                               f"Оставшееся количество: {data['col']} шт\n"
                                                               f"Дата прибытия: {data['date'].strftime('%d.%m.%Y')}",
                                                reply_markup=items_order_kb())
    await callback.answer()

# Add to basket
@router.callback_query(AddItemsISCF.filter(F.buy_now==False))
async def add_item_callbacks(callback: CallbackQuery, callback_data: AddItemsISCF, state: FSMContext) -> None:
    row = await db_inst.get_specific_row(callback_data.item_add_id)
    name = row[1]

    await db_basket.add_item_to_basket(callback.from_user.id, name, "inst")
    await state.set_state(OrderInfo.count_inst)
    await callback.message.answer(f"Напишите количество, которое вы хотели бы заказать", reply_markup=back_to_menu_kb())
    await callback.answer()

@router.callback_query(AddItemsISCF.filter(F.buy_now==True))
async def add_item_callbacks(callback: CallbackQuery, callback_data: AddItemsISCF, state: FSMContext) -> None:
    row = await db_inst.get_specific_row(callback_data.item_add_id)
    name = row[1]

    await db_basket.add_item_to_basket(callback.from_user.id, name, "inst")
    await state.set_state(OrderInfo.count_buy_now_inst)
    await callback.message.answer(f"Напишите количество, которое вы хотели бы заказать", reply_markup=back_to_menu_kb())
    await callback.answer()

@router.message(OrderInfo.count_inst)
async def count(msg: Message, state: FSMContext) -> None:
    name = await db_basket.get_name_item_where_null(msg.from_user.id)
    row = await db_inst.get_row_by_name(name)
    count = row[6]
    mult = row[7]
    min = row[8]

    if min is not None and mult is None:
        if (int(msg.text) <= count and int(msg.text) >= min) or (count <= min and int(msg.text) > 0 and int(msg.text) <= count):
            await db_basket.add_items_count(int(msg.text), msg.from_user.id)
            await state.clear()
            await msg.answer(f"Товар успешно добавлен в корзину!",
                                                    reply_markup=add_basket_kb())
        elif int(msg.text) < min and int(msg.text) >= 0:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели количество, меньшее, чем необходимый минимум!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        elif int(msg.text) < 0:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели отрицательное количество!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        else:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели количество, большее того, что есть в наличии!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                                          reply_markup=back_to_menu_kb())
    elif mult is not None and min is None:
        if (int(msg.text) % mult == 0 and int(msg.text) <= count and int(msg.text) > 0) or (count <= mult and int(msg.text) > 0 and int(msg.text) <= count):
            await db_basket.add_items_count(int(msg.text), msg.from_user.id)
            await state.clear()
            await msg.answer(f"Товар успешно добавлен в корзину!",
                                                    reply_markup=add_basket_kb())
        elif int(msg.text) < 0:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели отрицательное количество!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        elif int(msg.text) > count:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели количество, большее того, что есть в наличии!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                                          reply_markup=back_to_menu_kb())
        else:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели количество, которое не кратно, описанной выше кратности!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
    elif min is not None and mult is not None:
        if int(msg.text) <= count and int(msg.text) >= min and int(msg.text)%mult == 0:
            await db_basket.add_items_count(int(msg.text), msg.from_user.id)
            await state.clear()
            await msg.answer(f"Товар успешно добавлен в корзину!",
                                                    reply_markup=add_basket_kb())
        elif int(msg.text) < 0:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели отрицательное количество!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        elif int(msg.text) > count:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели количество, большее того, что есть в наличии!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                                          reply_markup=back_to_menu_kb())
        elif int(msg.text)%mult != 0:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели количество, которое не кратно, описанной выше кратности!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        elif int(msg.text) < min and int(msg.text) >= 0:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели количество, меньшее, чем необходимый минимум!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        else:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели количество, большее того, что есть в наличии!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                                          reply_markup=back_to_menu_kb())

@router.message(OrderInfo.count_buy_now_inst)
async def count(msg: Message, state: FSMContext) -> None:
    name = await db_basket.get_name_item_where_null(msg.from_user.id)
    row = await db_inst.get_row_by_name(name)
    count = row[6]
    mult = row[7]
    min = row[8]

    if min is not None and mult is None:
        if (int(msg.text) <= count and int(msg.text) >= min) or (count <= min and int(msg.text) > 0 and int(msg.text) <= count):
            await db_basket.add_items_count(int(msg.text), msg.from_user.id)
            await state.clear()
            await db_ord.add_user_to_order(msg.from_user.id)
            reg_info = await db_ord.get_ord_row(msg.from_user.id)
            if reg_info[2] is None:
                await msg.answer(f"Выберите тип вашего бизнеса", reply_markup=business_type_kb())
            else:
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
                                     f"{pre_ord[0]}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
                elif pre_order_exist and not items_otw_exist and not items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Предзаказ:</b>\n"
                                     f"{pre_ord[0]}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
                elif not pre_order_exist and items_otw_exist and not items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
                elif pre_order_exist and not items_otw_exist and items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                     f"<b>Предзаказ:</b>\n"
                                     f"{pre_ord[0]}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                    reply_markup=send_order_kb())
                elif not pre_order_exist and not items_otw_exist and items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
                elif pre_order_exist and items_otw_exist and items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                     f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                     f"<b>Предзаказ:</b>\n"
                                     f"{pre_ord[0]}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                    reply_markup=send_order_kb())
                elif not pre_order_exist and items_otw_exist and items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                     f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
        elif int(msg.text) < min and int(msg.text) >= 0:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели количество, меньшее, чем необходимый минимум!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        elif int(msg.text) < 0:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели отрицательное количество!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        else:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели количество, большее того, что есть в наличии!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
    elif mult is not None and min is None:
        if (int(msg.text) % mult == 0 and int(msg.text) <= count and int(msg.text) > 0) or (count <= mult and int(msg.text) > 0 and int(msg.text) <= count):
            await db_basket.add_items_count(int(msg.text), msg.from_user.id)
            await state.clear()
            await db_ord.add_user_to_order(msg.from_user.id)
            reg_info = await db_ord.get_ord_row(msg.from_user.id)
            if reg_info[2] is None:
                await msg.answer(f"Выберите тип вашего бизнеса", reply_markup=business_type_kb())
            else:
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
                                     f"{pre_ord[0]}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
                elif pre_order_exist and not items_otw_exist and not items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Предзаказ:</b>\n"
                                     f"{pre_ord[0]}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
                elif not pre_order_exist and items_otw_exist and not items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
                elif pre_order_exist and not items_otw_exist and items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                     f"<b>Предзаказ:</b>\n"
                                     f"{pre_ord[0]}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
                elif not pre_order_exist and not items_otw_exist and items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
                elif pre_order_exist and items_otw_exist and items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                     f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                     f"<b>Предзаказ:</b>\n"
                                     f"{pre_ord[0]}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
                elif not pre_order_exist and items_otw_exist and items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                     f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
        elif int(msg.text) < 0:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели отрицательное количество!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        elif int(msg.text) > count:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели количество, большее того, что есть в наличии!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        else:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели количество, которое не кратно, описанной выше кратности!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())

    elif min is not None and mult is not None:
        if int(msg.text) <= count and int(msg.text) >= min and int(msg.text)%mult == 0:
            await db_basket.add_items_count(int(msg.text), msg.from_user.id)
            await state.clear()
            await db_ord.add_user_to_order(msg.from_user.id)
            reg_info = await db_ord.get_ord_row(msg.from_user.id)
            if reg_info[2] is None:
                await msg.answer(f"Выберите тип вашего бизнеса", reply_markup=business_type_kb())
            else:
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
                                     f"{pre_ord[0]}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
                elif pre_order_exist and not items_otw_exist and not items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Предзаказ:</b>\n"
                                     f"{pre_ord[0]}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
                elif not pre_order_exist and items_otw_exist and not items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
                elif pre_order_exist and not items_otw_exist and items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                     f"<b>Предзаказ:</b>\n"
                                     f"{pre_ord[0]}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
                elif not pre_order_exist and not items_otw_exist and items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
                elif pre_order_exist and items_otw_exist and items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                     f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                     f"<b>Предзаказ:</b>\n"
                                     f"{pre_ord[0]}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
                elif not pre_order_exist and items_otw_exist and items_inst_exist:
                    await msg.answer(f"<u><b>Корзина</b></u>\n\n"
                                     f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                     f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                     f"<b>Данные о вас:</b>\n"
                                     f"Тип бизнеса: {reg_info[2]}\n"
                                     f"ФИО: {reg_info[3]}\n"
                                     f"Номер телефона: {reg_info[4]}",
                                     reply_markup=send_order_kb())
        elif int(msg.text) < 0:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели отрицательное количество!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        elif int(msg.text) > count:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели количество, большее того, что есть в наличии!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                                          reply_markup=back_to_menu_kb())
        elif int(msg.text)%mult != 0:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели количество, которое не кратно, описанной выше кратности!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        elif int(msg.text) < min and int(msg.text) >= 0:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели количество, меньшее, чем необходимый минимум!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                             reply_markup=back_to_menu_kb())
        else:
            await state.set_state(OrderInfo.count_inst)
            await msg.answer(f"<b>Вы ввели количество, большее того, что есть в наличии!</b>\n\n"
                             f"Напишите количество, которое вы хотели бы заказать еще раз",
                                          reply_markup=back_to_menu_kb())
