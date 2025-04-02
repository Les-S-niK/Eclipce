## Pip modules:
from sqlalchemy import select

## Project modules:
from core.async_database.db_engine import session_factory, engine
from core.async_database.db_models import Users, Base

## Create tables
async def create_tables():
    """Create all tables"""
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
## Delete tables
async def delete_tables():
    """Delete all tables"""
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)


class Hook:

    async def append(self, **kwargs):
        """Append element in table

        Args:
            table (str): name of table (users/)
            **kwargs: data (login/hashed_password)
        """
        try:
            async with session_factory() as session:
                user: Users = Users(login=kwargs["login"], hashed_pass=kwargs["hashed_password"])
                session.add(user)
                await session.commit()
                return True
                    
        except Exception:
            await session.commit()
            return False
                
    async def remove(self, all: bool = False, **flag):
        """Remove element in table

        Args:
            **flag: selector (id/login/hashed_password)
        """
        try:
            async with session_factory() as session:
                query = select(Users).filter_by(**flag)
                result = await session.execute(query)
                users = result.scalars().first() if all is False else result.scalars().all()
                for user in users: 
                    await session.delete(user)
                await session.commit()
                return True

        except Exception:
            await session.commit()
            return False
    
    async def get(self, table: str = None, _one_object: bool = False, **flag):
        """Get element in table

        Args:
            obj (bool): set true if you wanna return user object
            **flag: selector (id/login/hashed_password)
        """
        try:
            async with session_factory() as session:
                query = select(Users).filter_by(**flag)
                result = await session.execute(query)
                users = result.scalars().all()
                if not to_obj:
                    await session.commit()
                    return [
                        {"id": user.id, "login": user.login, "hashed_pass": user.hashed_pass} 
                    for user in users]
                else: 
                    await session.commit()
                    return users

        except Exception as error:
            await session.commit()
            return error
            
    async def replace(self, object, all: bool = True, **flag):
        """Replace info in object

        Args:
            object (): object of element
            **flag: selector (id/login/hashed_password)
        """
        try:
            async with session_factory() as session:
                for obj in object:
                    session.add(obj)
                    for key, value in flag.items():
                        setattr(obj, key, value)
                    if all is False:
                        await session.commit()
                        return True
                await session.commit()
                return True
                    
        except Exception as error:
            await session.commit()   
            return error