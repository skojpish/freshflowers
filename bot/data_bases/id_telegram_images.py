from bot.data_bases.psql_conn import DB_conn

class DB_images_id(DB_conn):
    async def add_image_otw(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    row = await conn.fetchrow(f"SELECT * FROM administration_item WHERE col=0;")
                    if row is not None:
                        await conn.execute(f"INSERT INTO administration_telegramidimage (name, id_image) "
                                       f"VALUES ('{row[1]}', '{row[10]}');")
                    else:
                        pass
        except:
            print('MDA')

    async def add_image_inst(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    row = await conn.fetchrow(f"SELECT * FROM administration_instock WHERE col=0;")
                    if row is not None:
                        await conn.execute(f"INSERT INTO administration_telegramidimage (name, id_image) "
                                       f"VALUES ('{row[1]}', '{row[10]}');")
                    else:
                        pass
        except:
            print('MDA')


db_tg_image = DB_images_id()
