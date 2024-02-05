from bot.data_bases.psql_conn import DB_conn

class DB_inst(DB_conn):
    async def get_category_data10(self, category):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    rows = await conn.fetch(f"SELECT * FROM administration_instock WHERE category='{category}' AND "
                                            f"(photo!='' OR image_id IS NOT NULL) ORDER BY id LIMIT 10;")
        except:
            print('MDA')
        else:
            return rows

    async def get_category_data_more(self, category, offset):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    rows = await conn.fetch(f"SELECT * FROM administration_instock WHERE category='{category}' AND "
                                            f"(photo!='' OR image_id IS NOT NULL) ORDER BY id LIMIT 10 OFFSET {offset};")
        except:
            print('MDA')
        else:
            return rows

    async def get_specific_row(self, item_id):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    row = await conn.fetchrow(f"SELECT * FROM administration_instock WHERE id={item_id};")
        except:
            print('MDA')
        else:
            return row

    async def get_rows_count_category(self, category):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    data = await conn.execute(f"SELECT * FROM administration_instock WHERE category='{category}';")
                    rows_count = int(data[7])+1
        except:
            print('MDA')
        else:
            return rows_count

    async def get_categories(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    data = await conn.fetch(f"SELECT category FROM administration_instock WHERE photo!='' OR image_id!='';")
                    categories = []
                    for i in range(len(data)):
                        if data[i][0] in categories:
                            pass
                        else:
                            categories.append(data[i][0])
        except:
            print("MDA")
        else:
            return categories

    async def add_image_id(self, item_id, image_id, name_image_id):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE administration_instock SET image_id='{image_id}', "
                                       f"name_image_id='{name_image_id}' WHERE id='{item_id}';")
        except:
            print("MDA")

    async def change_col(self, col, name):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE administration_instock SET col=col-{col} WHERE name=$1;", name)
        except:
            print("MDA")

    async def delete_item(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"DELETE FROM administration_instock WHERE col=0;")
        except:
            print("MDA")

    async def get_row_by_name(self, name):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    row = await conn.fetchrow(f"SELECT * FROM administration_instock WHERE name=$1;", name)
        except:
            print("MDA")
        else:
            return row


db_inst = DB_inst()
