from sql_hooks.db_requests import delete_tables, create_tables
import asyncio

async def a():
    await delete_tables()
    
asyncio.run(a())