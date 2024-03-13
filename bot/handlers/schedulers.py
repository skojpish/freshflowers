import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.config import bot
from bot.data_bases.basket import db_basket
from bot.data_bases.mailings import db_mail
from bot.data_bases.psql_get import db_otw
from bot.keyboards.menu_kbs import scheduler_kb

scheduler = AsyncIOScheduler()

async def start_scheduler():
    scheduler.configure({'apscheduler.daemon': False})
    scheduler.start()
    scheduler.add_job(check_mailings, 'interval', minutes=15)

async def check_mailings():

    await db_otw.check_date()

    mails = await db_mail.get_mails()

    if mails:
        for mail in mails:
            date_time = mail[2]
            mail_id = mail[0]

            scheduler.add_job(send_mailing, "date", run_date=date_time, kwargs={'mail_id': mail_id},
                              timezone='Europe/Moscow')

            await db_mail.update_mail_status(mail_id)



async def send_mailing(mail_id):
    text = await db_mail.get_mail_by_id(mail_id)

    # if text:
    #     users = await db_basket.get_all_users()
    #     counter = 0
    #
    #     for user_id in users:
    #         if counter % 10 == 0:
    #             await asyncio.sleep(1)
    #
    #         try:
    #             await bot.send_message(user_id[0],
    #                                    text[0],
    #                                    reply_markup=scheduler_kb())
    #         except:
    #             pass
    #
    #         counter += 1

    # TEST
    if text:
        users = [317325310, 1457515423]
        #users = [317325310, 317325310, 317325310, 317325310, 317325310,
        # 317325310, 317325310, 317325310, 317325310, 317325310,
        # 317325310, 317325310, 317325310, 317325310, 317325310]

        counter = 0

        for user_id in users:
            if counter % 10 == 0:
                await asyncio.sleep(1)

            try:
                await bot.send_message(user_id,
                                       text[0],
                                       reply_markup=scheduler_kb())
            except:
                pass

            counter += 1
