from bot.data_bases.psql_conn import DB_conn
from .config_logger_db import logger

class DB_mailings(DB_conn):
    async def get_mails(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    rows = await conn.fetch(f"SELECT * FROM administration_mailing WHERE status_new=True;")
        except Exception as e:
            logger.error(e)
        else:
            return rows

    async def update_mail_status(self, mail_id):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE administration_mailing SET status_new=False WHERE id={mail_id};")
        except Exception as e:
            logger.error(e)

    async def get_mail_by_id(self, mail_id):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    row = await conn.fetchrow(f"SELECT mail_text FROM administration_mailing WHERE id={mail_id};")
        except Exception as e:
            logger.error(e)
        else:
            return row

db_mail = DB_mailings()
