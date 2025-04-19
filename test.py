from core.async_database.db_crud import create_tables, delete_tables
import asyncio

async def main():
    await delete_tables()
    await create_tables()
    
asyncio.run(main())

