## Pip modules:
from sqlalchemy import select

## Project modules:
from sql_hooks.db_engine import session_factory, engine
from sql_hooks.db_models import Users, Base

## Create tables
async def create_tables():
    """Create all tables
    """
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
## Delete tables
async def delete_tables():
    """Delete all tables
    """
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
## SQL hooks
class Hook:
    
    def __init__(self, table: str = None):
        self.table = table

    async def append(self, table: str = None, **kwargs):
        """Append element in table

        Args:
            table (str): name of table (users/)
            **kwargs: data (username/login/hash)
        """
        current_table: str = self.table if table is None else table
        try:
            async with session_factory() as session:
                if current_table == "users":
                    user: Users = Users(username=kwargs["username"], login=kwargs["login"], hash=kwargs["hash"])
                    session.add(user)
                    await session.commit()
                    return True
                
                else:
                    await session.commit()
                    return None
                    
        except Exception as e:
            await session.commit()
            return e
                
    async def remove(self, table: str = None, all: bool = False, **flag):
        """Remove element in table

        Args:
            table (str): name of table (users/)
            **flag: selector (id/username/login/hash)
        """
        current_table: str = self.table if table is None else table
        try:
            async with session_factory() as session:
                if current_table == "users":
                        query = select(Users).filter_by(**flag)
                        result = await session.execute(query)
                        users = result.scalars().first() if all is False else result.scalars().all()
                        if users:
                            for user in users: 
                                await session.delete(user)
                            await session.commit()
                            return True
                        else:
                            await session.commit()
                            return None
                        
                else:
                    await session.commit()
                    return None
                        
        except Exception as e:
            await session.commit()
            return e
    
    async def get(self, table: str = None, to_obj: bool = False, **flag):
        """Get element in table

        Args:
            table (str): name of table (users/)
            obj (bool): set true if you wanna return user object
            **flag: selector (id/username/login/hash)
        """
        current_table: str = self.table if table is None else table
        try:
            async with session_factory() as session:
                if current_table == "users":
                        query = select(Users).filter_by(**flag)
                        result = await session.execute(query)
                        users = result.scalars().all()
                        if users:
                            if not to_obj:
                                session.commit()
                                return [
                                    {"id": user.id, "username": user.username, "login": user.login, "hash": user.hash} 
                                for user in users]
                            else: 
                                await session.commit()
                                return users
                        else:
                            await session.commit()
                            return None
                        
                else:
                    await session.commit()
                    return None
                        
        except Exception as e:
            await session.commit()
            return e
            
    async def replace(self, object, all: bool = True, table: str = None, **flag):
        """Replace info in object

        Args:
            table (str): name of table (users/)
            object (): object of element
            **flag: selector (id/username/login/hash)
        """
        current_table: str = self.table if table is None else table
        try:
            async with session_factory() as session:
                if current_table == "users":
                    for obj in object:
                        session.add(obj)
                        for key, value in flag.items():
                            setattr(obj, key, value)
                        if all is False:
                            await session.commit()
                            return True
                    await session.commit()
                    return True
                
                else:
                    await session.commit()
                    return None
                    
        except Exception as e:
            await session.commit()   
            return e 