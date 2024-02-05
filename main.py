import asyncio

from aiogram import Dispatcher

from bot.config import bot
from bot.data_bases.basket import db_basket
from bot.data_bases.order import db_ord
from bot.handlers import order_handlers, otw_handlers, bot_commands, edit_handlers, in_stock_handlers
from bot.handlers.bot_commands import setup_bot_commands


# добавить хэндлеры товаров в наличии и шедулер!!

async def main() -> None:
    dp = Dispatcher()

    dp.include_routers(otw_handlers.router, order_handlers.router, bot_commands.router, edit_handlers.router,
                       in_stock_handlers.router)

    try:
        await setup_bot_commands()
        await db_ord.create_order_table()
        await db_basket.create_basket_table()
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except:
        print("there is an exception")


if __name__ == "__main__":
    asyncio.run(main())
