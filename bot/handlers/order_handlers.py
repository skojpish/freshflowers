from glob import glob

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from bot.config import bot, master_id1, master_username1, master_id2, master_username2
from bot.data_bases.basket import db_basket
from bot.data_bases.fsm import PreOrder, OrderConfirm
from bot.data_bases.id_telegram_images import db_tg_image
from bot.data_bases.in_stock import db_inst
from bot.data_bases.order import db_ord
from bot.data_bases.psql_get import db_otw
from bot.keyboards.menu_kbs import back_to_menu_kb, back_to_menu_photo_kb
from bot.keyboards.order_kbs import basket_kb, add_basket_kb, business_type_kb, preord_kb, \
    basket_empty_kb, continue_kb, send_order_kb

from datetime import datetime

router = Router()

# Menu
@router.callback_query(F.data == "about")
async def about(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Какой-то текст")
    await callback.message.edit_reply_markup(reply_markup=back_to_menu_kb())

@router.callback_query(F.data == "channel")
async def channel(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Ссылка на канал и описание")
    await callback.message.edit_reply_markup(reply_markup=back_to_menu_kb())

@router.callback_query(F.data == "price_list")
async def price_list(callback: CallbackQuery) -> None:
    await callback.message.delete()
    files = glob(f"django_admin/proj/media/pricelist/*")
    if len(files) != 0:
        file = files[0]
        doc = FSInputFile(file)
        await callback.message.answer_document(doc, caption='Прайс лист актуальных позиций',
                                               reply_markup=back_to_menu_photo_kb())
    else:
        await callback.message.answer('Прайс лист будет загружен позже! Извините за неудобства',
                                      reply_markup=back_to_menu_kb())

# Basket
@router.callback_query(F.data == "basket")
async def basket(callback: CallbackQuery) -> None:
    items_otw = []
    items_inst = []
    pre_ord = []
    items_otw_exist: bool = False
    items_inst_exist: bool = False
    pre_order_exist: bool = False

    basket_data = await db_basket.print_basket(callback.from_user.id)
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
        await callback.message.edit_text(f"<u><b>Корзина</b></u>\n\n"
                                         f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                      f"<b>Предзаказ:</b>\n"
                                      f"{pre_ord[0]}")
        await callback.message.edit_reply_markup(reply_markup=basket_kb())
    elif pre_order_exist and not items_otw_exist and not items_inst_exist:
        await callback.message.edit_text(f"<u><b>Корзина</b></u>\n\n"
                                      f"<b>Предзаказ:</b>\n"
                                      f"{pre_ord[0]}")
        await callback.message.edit_reply_markup(reply_markup=basket_kb())
    elif not pre_order_exist and items_otw_exist and not items_inst_exist:
        await callback.message.edit_text(f"<u><b>Корзина</b></u>\n\n"
            f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}")
        await callback.message.edit_reply_markup(reply_markup=basket_kb())
    elif pre_order_exist and not items_otw_exist and items_inst_exist:
        await callback.message.edit_text(f"<u><b>Корзина</b></u>\n\n"
                                         f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                         f"<b>Предзаказ:</b>\n"
                                         f"{pre_ord[0]}")
        await callback.message.edit_reply_markup(reply_markup=basket_kb())
    elif not pre_order_exist and not items_otw_exist and items_inst_exist:
        await callback.message.edit_text(f"<u><b>Корзина</b></u>\n\n"
            f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}")
        await callback.message.edit_reply_markup(reply_markup=basket_kb())
    elif pre_order_exist and items_otw_exist and items_inst_exist:
        await callback.message.edit_text(f"<u><b>Корзина</b></u>\n\n"
                                         f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                         f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                         f"<b>Предзаказ:</b>\n"
                                         f"{pre_ord[0]}")
        await callback.message.edit_reply_markup(reply_markup=basket_kb())
    elif not pre_order_exist and items_otw_exist and items_inst_exist:
        await callback.message.edit_text(f"<u><b>Корзина</b></u>\n\n"
                                         f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                         f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}")
        await callback.message.edit_reply_markup(reply_markup=basket_kb())
    else:
        await callback.message.edit_text(f"Корзина пуста")
        await callback.message.edit_reply_markup(reply_markup=basket_empty_kb())
    await callback.answer()

# Delete basket
@router.callback_query(F.data == "delete_basket")
async def delete_basket(callback: CallbackQuery) -> None:
    await db_basket.delete_user_basket(callback.from_user.id)
    await callback.message.edit_text("Корзина пуста")
    await callback.message.edit_reply_markup(reply_markup=basket_empty_kb())
    await callback.answer()

# Continue shopping
@router.callback_query(F.data == "continue")
async def continue_shopping(callback: CallbackQuery) -> None:
    await callback.message.edit_text(f"Выберите категорию")
    await callback.message.edit_reply_markup(reply_markup=continue_kb())
    await callback.answer()

# Pre-order handlers
@router.callback_query(F.data == "pre_order")
async def pre_order(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(PreOrder.desc)
    await callback.message.edit_text(f"Опишите в свободной форме ваш заказ в ОДНОМ сообщении")
    await callback.message.edit_reply_markup(reply_markup=back_to_menu_kb())
    await callback.answer()

# Order registration
@router.callback_query(F.data == "reg_order")
async def confirm_pre_order(callback: CallbackQuery) -> None:
    await db_ord.add_user_to_order(callback.from_user.id)
    reg_info = await db_ord.get_ord_row(callback.from_user.id)
    if reg_info[2] is None:
        await callback.message.edit_text(f"Выберите тип вашего бизнеса")
        await callback.message.edit_reply_markup(reply_markup=business_type_kb())
    else:
        items_otw = []
        items_inst = []
        pre_ord = []
        items_otw_exist: bool = False
        items_inst_exist: bool = False
        pre_order_exist: bool = False

        basket_data = await db_basket.print_basket(callback.from_user.id)
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
            await callback.message.edit_text(f"<u><b>Заявка</b></u>\n\n"
                                             f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                             f"<b>Предзаказ:</b>\n"
                                             f"{pre_ord[0]}\n\n"
                                             f"<b>Данные о вас:</b>\n"
                                             f"Тип бизнеса: {reg_info[2]}\n"
                                             f"ФИО: {reg_info[3]}\n"
                                             f"Номер телефона: {reg_info[4]}")
            await callback.message.edit_reply_markup(reply_markup=send_order_kb())
        elif pre_order_exist and not items_otw_exist and not items_inst_exist:
            await callback.message.edit_text(f"<u><b>Заявка</b></u>\n\n"
                                             f"<b>Предзаказ:</b>\n"
                                             f"{pre_ord[0]}\n\n"
                                             f"<b>Данные о вас:</b>\n"
                                             f"Тип бизнеса: {reg_info[2]}\n"
                                             f"ФИО: {reg_info[3]}\n"
                                             f"Номер телефона: {reg_info[4]}")
            await callback.message.edit_reply_markup(reply_markup=send_order_kb())
        elif not pre_order_exist and items_otw_exist and not items_inst_exist:
            await callback.message.edit_text(f"<u><b>Заявка</b></u>\n\n"
                                             f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                             f"<b>Данные о вас:</b>\n"
                                             f"Тип бизнеса: {reg_info[2]}\n"
                                             f"ФИО: {reg_info[3]}\n"
                                             f"Номер телефона: {reg_info[4]}")
            await callback.message.edit_reply_markup(reply_markup=send_order_kb())
        elif pre_order_exist and not items_otw_exist and items_inst_exist:
            await callback.message.edit_text(f"<u><b>Заявка</b></u>\n\n"
                                             f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                             f"<b>Предзаказ:</b>\n"
                                             f"{pre_ord[0]}\n\n"
                                             f"<b>Данные о вас:</b>\n"
                                             f"Тип бизнеса: {reg_info[2]}\n"
                                             f"ФИО: {reg_info[3]}\n"
                                             f"Номер телефона: {reg_info[4]}")
            await callback.message.edit_reply_markup(reply_markup=send_order_kb())
        elif not pre_order_exist and not items_otw_exist and items_inst_exist:
            await callback.message.edit_text(f"<u><b>Заявка</b></u>\n\n"
                                             f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                             f"<b>Данные о вас:</b>\n"
                                             f"Тип бизнеса: {reg_info[2]}\n"
                                             f"ФИО: {reg_info[3]}\n"
                                             f"Номер телефона: {reg_info[4]}")
            await callback.message.edit_reply_markup(reply_markup=send_order_kb())
        elif pre_order_exist and items_otw_exist and items_inst_exist:
            await callback.message.edit_text(f"<u><b>Заявка</b></u>\n\n"
                                             f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                             f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                             f"<b>Предзаказ:</b>\n"
                                             f"{pre_ord[0]}\n\n"
                                             f"<b>Данные о вас:</b>\n"
                                             f"Тип бизнеса: {reg_info[2]}\n"
                                             f"ФИО: {reg_info[3]}\n"
                                             f"Номер телефона: {reg_info[4]}")
            await callback.message.edit_reply_markup(reply_markup=send_order_kb())
        elif not pre_order_exist and items_otw_exist and items_inst_exist:
            await callback.message.edit_text(f"<u><b>Заявка</b></u>\n\n"
                                             f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                             f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                             f"<b>Данные о вас:</b>\n"
                                             f"Тип бизнеса: {reg_info[2]}\n"
                                             f"ФИО: {reg_info[3]}\n"
                                             f"Номер телефона: {reg_info[4]}")
            await callback.message.edit_reply_markup(reply_markup=send_order_kb())
    await callback.answer()

# Choice type of business
@router.callback_query(F.data == "person")
async def type_person(callback: CallbackQuery, state: FSMContext) -> None:
    await db_ord.add_user_to_order(callback.from_user.id)
    await db_ord.add_bus_type(callback.from_user.id, 'Частное лицо')
    await state.set_state(OrderConfirm.full_name)
    await callback.message.edit_text(f"Напишите ваши фамилию, имя и отчество")
    await callback.message.edit_reply_markup(reply_markup=back_to_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "shop")
async def type_shop(callback: CallbackQuery, state: FSMContext) -> None:
    await db_ord.add_user_to_order(callback.from_user.id)
    await db_ord.add_bus_type(callback.from_user.id, 'Магазин')
    await state.set_state(OrderConfirm.full_name)
    await callback.message.edit_text(f"Напишите ваши фамилию, имя и отчество")
    await callback.message.edit_reply_markup(reply_markup=back_to_menu_kb())
    await callback.answer()

# Pre-order add to basket
@router.callback_query(F.data == "add_preord_to_basket")
async def confirm_pre_order(callback: CallbackQuery) -> None:
    await callback.message.edit_text(f"Предзаказ успешно добавлен  в корзину!")
    await callback.message.edit_reply_markup(reply_markup=add_basket_kb())
    await callback.answer()

# Pre-order states
@router.message(PreOrder.desc)
async def order_desc(msg: Message, state: FSMContext) -> None:
    await db_basket.add_pre_order_to_basket(msg.from_user.id, msg.text)
    await state.clear()
    await msg.answer(f"<b>Вы ввели следующую информацию по предзаказу:</b>\n"
                     f"{msg.text}", reply_markup=preord_kb())

# Order states
@router.message(OrderConfirm.full_name)
async def order_fname(msg: Message, state: FSMContext) -> None:
    await db_ord.add_full_name(msg.from_user.id, msg.text)
    await state.clear()
    await state.set_state(OrderConfirm.number)
    await msg.answer("Напишите ваш номер телефона", reply_markup=back_to_menu_kb())

@router.message(OrderConfirm.number)
async def order_number(msg: Message, state: FSMContext) -> None:
    await db_ord.add_number(msg.from_user.id, msg.text)
    await state.clear()

    reg_info = await db_ord.get_ord_row(msg.from_user.id)

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
        await msg.answer(f"<u><b>Заявка</b></u>\n\n"
                         f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                         f"<b>Предзаказ:</b>\n"
                         f"{pre_ord[0]}\n\n"
                         f"<b>Данные о вас:</b>\n"
                         f"Тип бизнеса: {reg_info[2]}\n"
                         f"ФИО: {reg_info[3]}\n"
                         f"Номер телефона: {reg_info[4]}",
                         reply_markup=send_order_kb())
    elif pre_order_exist and not items_otw_exist and not items_inst_exist:
        await msg.answer(f"<u><b>Заявка</b></u>\n\n"
                         f"<b>Предзаказ:</b>\n"
                         f"{pre_ord[0]}\n\n"
                         f"<b>Данные о вас:</b>\n"
                         f"Тип бизнеса: {reg_info[2]}\n"
                         f"ФИО: {reg_info[3]}\n"
                         f"Номер телефона: {reg_info[4]}",
                         reply_markup=send_order_kb())
    elif not pre_order_exist and items_otw_exist and not items_inst_exist:
        await msg.answer(f"<u><b>Заявка</b></u>\n\n"
                         f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                         f"<b>Данные о вас:</b>\n"
                         f"Тип бизнеса: {reg_info[2]}\n"
                         f"ФИО: {reg_info[3]}\n"
                         f"Номер телефона: {reg_info[4]}",
                         reply_markup=send_order_kb())
    elif pre_order_exist and not items_otw_exist and items_inst_exist:
        await msg.answer(f"<u><b>Заявка</b></u>\n\n"
                         f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                         f"<b>Предзаказ:</b>\n"
                         f"{pre_ord[0]}\n\n"
                         f"<b>Данные о вас:</b>\n"
                         f"Тип бизнеса: {reg_info[2]}\n"
                         f"ФИО: {reg_info[3]}\n"
                         f"Номер телефона: {reg_info[4]}",
                         reply_markup=send_order_kb())
    elif not pre_order_exist and not items_otw_exist and items_inst_exist:
        await msg.answer(f"<u><b>Заявка</b></u>\n\n"
                         f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                         f"<b>Данные о вас:</b>\n"
                         f"Тип бизнеса: {reg_info[2]}\n"
                         f"ФИО: {reg_info[3]}\n"
                         f"Номер телефона: {reg_info[4]}",
                         reply_markup=send_order_kb())
    elif pre_order_exist and items_otw_exist and items_inst_exist:
        await msg.answer(f"<u><b>Заявка</b></u>\n\n"
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
        await msg.answer(f"<u><b>Заявка</b></u>\n\n"
                         f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                         f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                         f"<b>Данные о вас:</b>\n"
                         f"Тип бизнеса: {reg_info[2]}\n"
                         f"ФИО: {reg_info[3]}\n"
                         f"Номер телефона: {reg_info[4]}",
                         reply_markup=send_order_kb())

# Send order
@router.callback_query(F.data == "send_order")
async def confirm_pre_order(callback: CallbackQuery) -> None:
    items_otw = []
    items_inst = []
    pre_ord = []
    items_otw_exist: bool = False
    items_inst_exist: bool = False
    pre_order_exist: bool = False

    basket_data = await db_basket.print_basket(callback.from_user.id)

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

            await db_otw.change_col(data['col'], data['item'])
            await db_tg_image.add_image_otw()
            await db_otw.delete_item()
        elif data['item'] is not None and data['category'] == 'inst' and data['pre_ord'] is None:
            items_inst_exist = True
            items_inst.append(f"{data['item']}: {data['col']} шт")

            await db_inst.change_col(data['col'], data['item'])
            await db_tg_image.add_image_inst()
            await db_inst.delete_item()
        else:
            pre_order_exist = True
            pre_ord.append(f"{data['pre_ord']}")

    await callback.message.answer(f"Спасибо за заказ {callback.from_user.full_name}!\n"
                                  f"Наш менеджер скоро свяжется с вами", reply_markup=basket_empty_kb())

    new_line = '\n'
    reg_info = await db_ord.get_ord_row(callback.from_user.id)

    user_data = {
        'type_of_b': reg_info[2],
        'fullname': reg_info[3],
        'number': reg_info[4]
    }


    if callback.from_user.username:
        if pre_order_exist and items_otw_exist and not items_inst_exist:
            await bot.send_message(master_id1, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"Ссылка: https://t.me/{callback.from_user.username}\n\n"
                                              f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                              f"<b>Предзаказ:</b>\n"
                                              f"{pre_ord[0]}\n\n"
                                              f"<b>Данные о пользователе:</b>\n"
                                              f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")
            await bot.send_message(master_id2, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                               f"Пользователь: {callback.from_user.full_name}\n"
                                               f"Ссылка: https://t.me/{callback.from_user.username}\n\n"
                                               f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                               f"<b>Предзаказ:</b>\n"
                                               f"{pre_ord[0]}\n\n"
                                               f"<b>Данные о пользователе:</b>\n"
                                               f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")

            order = f"Товары в пути:\n{new_line.join([str(item) for item in items_otw])}\n\n" \
                    f"Предзаказ:\n" \
                    f"{pre_ord[0]}\n\n"

            await db_ord.add_order_to_site(callback.from_user.full_name, f'https://t.me/{callback.from_user.username}', order, user_data['type_of_b'],
                                           user_data['fullname'], user_data['number'], datetime.now())

        elif pre_order_exist and not items_otw_exist and not items_inst_exist:
            await bot.send_message(master_id1, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"Ссылка: https://t.me/{callback.from_user.username}\n\n"
                                              f"<b>Предзаказ:</b>\n"
                                              f"{pre_ord[0]}\n\n"
                                              f"<b>Данные о пользователе:</b>\n"
                                              f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")
            await bot.send_message(master_id2, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                               f"Пользователь: {callback.from_user.full_name}\n"
                                               f"Ссылка: https://t.me/{callback.from_user.username}\n\n"
                                               f"<b>Предзаказ:</b>\n"
                                               f"{pre_ord[0]}\n\n"
                                               f"<b>Данные о пользователе:</b>\n"
                                               f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")

            order = f"Предзаказ:\n" \
                    f"{pre_ord[0]}\n\n"

            await db_ord.add_order_to_site(callback.from_user.full_name, f'https://t.me/{callback.from_user.username}',
                                           order, user_data['type_of_b'],
                                           user_data['fullname'], user_data['number'], datetime.now())

        elif not pre_order_exist and items_otw_exist and not items_inst_exist:
            await bot.send_message(master_id1, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"Ссылка: https://t.me/{callback.from_user.username}\n\n"
                                              f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                              f"<b>Данные о пользователе:</b>\n"
                                              f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")
            await bot.send_message(master_id2, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                               f"Пользователь: {callback.from_user.full_name}\n"
                                               f"Ссылка: https://t.me/{callback.from_user.username}\n\n"
                                               f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                               f"<b>Данные о пользователе:</b>\n"
                                               f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")

            order = f"Товары в пути:\n{new_line.join([str(item) for item in items_otw])}\n\n"

            await db_ord.add_order_to_site(callback.from_user.full_name, f'https://t.me/{callback.from_user.username}',
                                           order, user_data['type_of_b'],
                                           user_data['fullname'], user_data['number'], datetime.now())

        elif pre_order_exist and not items_otw_exist and items_inst_exist:
            await bot.send_message(master_id1, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"Ссылка: https://t.me/{callback.from_user.username}\n\n"
                                              f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                              f"<b>Предзаказ:</b>\n"
                                              f"{pre_ord[0]}\n\n"
                                              f"<b>Данные о пользователе:</b>\n"
                                              f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")
            await bot.send_message(master_id2, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                               f"Пользователь: {callback.from_user.full_name}\n"
                                               f"Ссылка: https://t.me/{callback.from_user.username}\n\n"
                                               f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                               f"<b>Предзаказ:</b>\n"
                                               f"{pre_ord[0]}\n\n"
                                               f"<b>Данные о пользователе:</b>\n"
                                               f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")

            order = f"Товары в наличии:\n{new_line.join([str(item) for item in items_inst])}\n\n" \
                    f"Предзаказ:\n" \
                    f"{pre_ord[0]}\n\n"

            await db_ord.add_order_to_site(callback.from_user.full_name, f'https://t.me/{callback.from_user.username}',
                                           order, user_data['type_of_b'],
                                           user_data['fullname'], user_data['number'], datetime.now())

        elif not pre_order_exist and not items_otw_exist and items_inst_exist:
            await bot.send_message(master_id1, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"Ссылка: https://t.me/{callback.from_user.username}\n\n"
                                              f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                              f"<b>Данные о пользователе:</b>\n"
                                              f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")
            await bot.send_message(master_id2, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                               f"Пользователь: {callback.from_user.full_name}\n"
                                               f"Ссылка: https://t.me/{callback.from_user.username}\n\n"
                                               f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                               f"<b>Данные о пользователе:</b>\n"
                                               f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")

            order = f"Товары в наличии:\n{new_line.join([str(item) for item in items_inst])}\n\n"

            await db_ord.add_order_to_site(callback.from_user.full_name, f'https://t.me/{callback.from_user.username}',
                                           order, user_data['type_of_b'],
                                           user_data['fullname'], user_data['number'], datetime.now())

        elif pre_order_exist and items_otw_exist and items_inst_exist:
            await bot.send_message(master_id1, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"Ссылка: https://t.me/{callback.from_user.username}\n\n"
                                              f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                              f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                              f"<b>Предзаказ:</b>\n"
                                              f"{pre_ord[0]}\n\n"
                                              f"<b>Данные о пользователе:</b>\n"
                                              f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")
            await bot.send_message(master_id2, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                               f"Пользователь: {callback.from_user.full_name}\n"
                                               f"Ссылка: https://t.me/{callback.from_user.username}\n\n"
                                               f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                               f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                               f"<b>Предзаказ:</b>\n"
                                               f"{pre_ord[0]}\n\n"
                                               f"<b>Данные о пользователе:</b>\n"
                                               f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")

            order = f"Товары в пути:\n{new_line.join([str(item) for item in items_otw])}\n\n" \
                    f"Товары в наличии:\n{new_line.join([str(item) for item in items_inst])}\n\n" \
                    f"Предзаказ:\n" \
                    f"{pre_ord[0]}\n\n"

            await db_ord.add_order_to_site(callback.from_user.full_name, f'https://t.me/{callback.from_user.username}',
                                           order, user_data['type_of_b'],
                                           user_data['fullname'], user_data['number'], datetime.now())

        elif not pre_order_exist and items_otw_exist and items_inst_exist:
            await bot.send_message(master_id1, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"Ссылка: https://t.me/{callback.from_user.username}\n\n"
                                              f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                              f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                              f"<b>Данные о пользователе:</b>\n"
                                              f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")
            await bot.send_message(master_id2, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                               f"Пользователь: {callback.from_user.full_name}\n"
                                               f"Ссылка: https://t.me/{callback.from_user.username}\n\n"
                                               f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                               f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                               f"<b>Данные о пользователе:</b>\n"
                                               f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")

            order = f"Товары в пути:\n{new_line.join([str(item) for item in items_otw])}\n\n" \
                    f"Товары в наличии:\n{new_line.join([str(item) for item in items_inst])}\n\n"

            await db_ord.add_order_to_site(callback.from_user.full_name, f'https://t.me/{callback.from_user.username}',
                                           order, user_data['type_of_b'],
                                           user_data['fullname'], user_data['number'], datetime.now())

    elif not callback.from_user.username:
        await callback.message.answer(f"Добрый день, {callback.from_user.full_name}! Получили вашу заявку, но, кажется, у вас закрытый аккаунт и мы не можем с вами связаться.\n"
                         f"Напишите пожалуйста нам в личные сообщения: {master_username1} или {master_username2} \n"
                         f"Спасибо за заказ!", reply_markup=basket_empty_kb())

        if pre_order_exist and items_otw_exist and not items_inst_exist:
            await bot.send_message(master_id1, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>\n\n"
                                              f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                              f"<b>Предзаказ:</b>\n"
                                              f"{pre_ord[0]}\n\n"
                                              f"<b>Данные о пользователе:</b>\n"
                                              f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")
            await bot.send_message(master_id2, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                               f"Пользователь: {callback.from_user.full_name}\n"
                                               f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>\n\n"
                                               f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                               f"<b>Предзаказ:</b>\n"
                                               f"{pre_ord[0]}\n\n"
                                               f"<b>Данные о пользователе:</b>\n"
                                               f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")

            order = f"Товары в пути:\n{new_line.join([str(item) for item in items_otw])}\n\n" \
                    f"Предзаказ:\n" \
                    f"{pre_ord[0]}\n\n"

            await db_ord.add_order_to_site(callback.from_user.full_name, 'Закрытый акк. должен написать в лс',
                                           order, user_data['type_of_b'],
                                           user_data['fullname'], user_data['number'], datetime.now())

        elif pre_order_exist and not items_otw_exist and not items_inst_exist:
            await bot.send_message(master_id1, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>\n\n"
                                              f"<b>Предзаказ:</b>\n"
                                              f"{pre_ord[0]}\n\n"
                                              f"<b>Данные о пользователе:</b>\n"
                                              f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")
            await bot.send_message(master_id2, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                               f"Пользователь: {callback.from_user.full_name}\n"
                                               f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>\n\n"
                                               f"<b>Предзаказ:</b>\n"
                                               f"{pre_ord[0]}\n\n"
                                               f"<b>Данные о пользователе:</b>\n"
                                               f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")

            order = f"Предзаказ:\n" \
                    f"{pre_ord[0]}\n\n"

            await db_ord.add_order_to_site(callback.from_user.full_name, 'Закрытый акк. должен написать в лс',
                                           order, user_data['type_of_b'],
                                           user_data['fullname'], user_data['number'], datetime.now())

        elif not pre_order_exist and items_otw_exist and not items_inst_exist:
            await bot.send_message(master_id1, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>\n\n"
                                              f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                              f"<b>Данные о пользователе:</b>\n"
                                              f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")
            await bot.send_message(master_id2, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                               f"Пользователь: {callback.from_user.full_name}\n"
                                               f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>\n\n"
                                               f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                               f"<b>Данные о пользователе:</b>\n"
                                               f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")

            order = f"Товары в пути:\n{new_line.join([str(item) for item in items_otw])}\n\n"

            await db_ord.add_order_to_site(callback.from_user.full_name, 'Закрытый акк. должен написать в лс',
                                           order, user_data['type_of_b'],
                                           user_data['fullname'], user_data['number'], datetime.now())

        elif pre_order_exist and not items_otw_exist and items_inst_exist:
            await bot.send_message(master_id1, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>\n\n"
                                              f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                              f"<b>Предзаказ:</b>\n"
                                              f"{pre_ord[0]}\n\n"
                                              f"<b>Данные о пользователе:</b>\n"
                                              f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")
            await bot.send_message(master_id2, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                               f"Пользователь: {callback.from_user.full_name}\n"
                                               f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>\n\n"
                                               f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                               f"<b>Предзаказ:</b>\n"
                                               f"{pre_ord[0]}\n\n"
                                               f"<b>Данные о пользователе:</b>\n"
                                               f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")

            order = f"Товары в наличии:\n{new_line.join([str(item) for item in items_inst])}\n\n" \
                    f"Предзаказ:\n" \
                    f"{pre_ord[0]}\n\n"

            await db_ord.add_order_to_site(callback.from_user.full_name, 'Закрытый акк. должен написать в лс',
                                           order, user_data['type_of_b'],
                                           user_data['fullname'], user_data['number'], datetime.now())

        elif not pre_order_exist and not items_otw_exist and items_inst_exist:
            await bot.send_message(master_id1, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>\n\n"
                                              f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                              f"<b>Данные о пользователе:</b>\n"
                                              f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")
            await bot.send_message(master_id2, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                               f"Пользователь: {callback.from_user.full_name}\n"
                                               f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>\n\n"
                                               f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                               f"<b>Данные о пользователе:</b>\n"
                                               f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")

            order = f"Товары в наличии:\n{new_line.join([str(item) for item in items_inst])}\n\n"

            await db_ord.add_order_to_site(callback.from_user.full_name, 'Закрытый акк. должен написать в лс',
                                           order, user_data['type_of_b'],
                                           user_data['fullname'], user_data['number'], datetime.now())

        elif pre_order_exist and items_otw_exist and items_inst_exist:
            await bot.send_message(master_id1, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>\n\n"
                                              f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                              f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                              f"<b>Предзаказ:</b>\n"
                                              f"{pre_ord[0]}\n\n"
                                              f"<b>Данные о пользователе:</b>\n"
                                              f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")
            await bot.send_message(master_id2, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                               f"Пользователь: {callback.from_user.full_name}\n"
                                               f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>\n\n"
                                               f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                               f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                               f"<b>Предзаказ:</b>\n"
                                               f"{pre_ord[0]}\n\n"
                                               f"<b>Данные о пользователе:</b>\n"
                                               f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")

            order = f"Товары в пути:\n{new_line.join([str(item) for item in items_otw])}\n\n" \
                    f"Товары в наличии:\n{new_line.join([str(item) for item in items_inst])}\n\n" \
                    f"Предзаказ:\n" \
                    f"{pre_ord[0]}\n\n"

            await db_ord.add_order_to_site(callback.from_user.full_name, 'Закрытый акк. должен написать в лс',
                                           order, user_data['type_of_b'],
                                           user_data['fullname'], user_data['number'], datetime.now())

        elif not pre_order_exist and items_otw_exist and items_inst_exist:
            await bot.send_message(master_id1, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>\n\n"
                                              f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                              f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                              f"<b>Данные о пользователе:</b>\n"
                                             f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")
            await bot.send_message(master_id2, f"<u><b>НОВЫЙ ЗАКАЗ</b></u>\n"
                                               f"Пользователь: {callback.from_user.full_name}\n"
                                               f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>\n\n"
                                               f"<b>Товары в пути:</b>\n{new_line.join([str(item) for item in items_otw])}\n\n"
                                               f"<b>Товары в наличии:</b>\n{new_line.join([str(item) for item in items_inst])}\n\n"
                                               f"<b>Данные о пользователе:</b>\n"
                                               f"Тип бизнеса: {user_data['type_of_b']}\n"
                                              f"ФИО: {user_data['fullname']}\n"
                                              f"Номер телефона: {user_data['number']}")

            order = f"Товары в пути:\n{new_line.join([str(item) for item in items_otw])}\n\n" \
                    f"Товары в наличии:\n{new_line.join([str(item) for item in items_inst])}\n\n"

            await db_ord.add_order_to_site(callback.from_user.full_name, 'Закрытый акк. должен написать в лс',
                                           order, user_data['type_of_b'],
                                           user_data['fullname'], user_data['number'], datetime.now())

    await db_basket.delete_user_basket(callback.from_user.id)
    await callback.answer()
