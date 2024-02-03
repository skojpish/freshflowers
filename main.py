import logging
import sys

from aiogram import Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from bot.config import bot
from bot.data_bases.basket import db_basket
from bot.data_bases.order import db_ord
from bot.data_bases.psql_get import db_otw
from bot.handlers import order_handlers, otw_handlers, bot_commands, edit_handlers, in_stock_handlers

from apscheduler.schedulers.asyncio import AsyncIOScheduler


WEB_SERVER_HOST = '127.0.0.1'
WEB_SERVER_PORT = 8080

WEBHOOK_PATH = '/webhook'
BASE_WEBHOOK_URL = f"xxx"


async def on_startup() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")
    await db_ord.create_order_table()
    await db_basket.create_basket_table()
    
    scheduler = AsyncIOScheduler()
    scheduler.configure({'apscheduler.daemon': False})
    scheduler.start()
    scheduler.add_job(db_otw.check_date, 'interval', minutes=15)


def main() -> None:
    dp = Dispatcher()

    dp.include_routers(otw_handlers.router, order_handlers.router, bot_commands.router, edit_handlers.router,
                       in_stock_handlers.router)

    dp.startup.register(on_startup)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
