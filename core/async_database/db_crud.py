## Pip modules:
from sqlalchemy import select
from sqlalchemy.exc import OperationalError

## Project modules:
from core.async_database.db_engine import session_factory, engine
from core.async_database.db_models import Users, Base, AsymmetricKeys

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
class UserHook:
    async def append(self, **kwargs):
        """Append element in table

        Args: 
            **kwargs: data (login/hashed_password)
        """
        try:
            async with session_factory() as session:
                user: Users = Users(login=kwargs["login"], hashed_password=kwargs["hashed_password"])
                session.add(user)
                await session.commit()
                return True

        except OperationalError:
            await session.rollback()
            return Users(**kwargs)
        except Exception:
            await session.rollback()
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
                users: Users = result.scalars().first() if all is False else result.scalars().all()
                for user in users: 
                    await session.delete(user)
                await session.commit()
                return True

        except Exception:
            await session.rollback()
            return False
    
    async def get(self, one_object: bool = False, **flag):
        """Get element in table

        Args:
            obj (bool): set true if you wanna return user object
            **flag: selector (id/login/hashed_password)
        """
        try:
            async with session_factory() as session:
                query = select(Users).filter_by(**flag)
                result = await session.execute(query)
                users: list[Users] = result.scalars().all()
                if one_object and users != []:
                    return users[0]
                return users

        except Exception:
            return False
            
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
                
                await session.commit()
                return True
                    
        except Exception as error:
            await session.rollback()   
            return error

class AsymmetricKeysHook:
    async def append(self, **kwargs):
        """Append element in table

        Args: 
            **kwargs: data (private_key/public_key)
        """
        try:
            async with session_factory() as session:
                key: AsymmetricKeys = AsymmetricKeys(public_key=kwargs["public_key"], private_key=kwargs["private_key"])
                session.add(key)
                await session.commit()
                return True

        except OperationalError:
            await session.rollback()
            return Users(**kwargs)
        except Exception:
            await session.rollback()
            return False
    
    async def remove(self, all: bool = False, **flag):
        """Remove element in table

        Args:
            **flag: selector (id/private_key/public_key)
        """
        try:
            async with session_factory() as session:
                query = select(AsymmetricKeys).filter_by(**flag)
                result = await session.execute(query)
                keys: AsymmetricKeys = result.scalars().first() if all is False else result.scalars().all()
                for key in keys: 
                    await session.delete(key)
                await session.commit()
                return True

        except Exception:
            await session.rollback()
            return False
        
    async def get(self, one_object: bool = False, **flag):
        """Get element in table

        Args:
            obj (bool): set true if you wanna return asymmetric_key object
            **flag: selector (id/private_key/public_key)
        """
        try:
            async with session_factory() as session:
                query = select(AsymmetricKeys).filter_by(**flag)
                result = await session.execute(query)
                keys: list[AsymmetricKeys] = result.scalars().all()
                if one_object and keys != []:
                    return keys[0]
                return keys

        except Exception:
            return False
        
    async def replace(self, object, all: bool = True, **flag):
        """Replace info in object

        Args:
            object (): object of element
            **flag: selector (id/private_key/public_key)
        """
        try:
            async with session_factory() as session:
                for obj in object:
                    session.add(obj)
                    for key, value in flag.items():
                        setattr(obj, key, value)
                
                await session.commit()
                return True
                    
        except Exception as error:
            await session.rollback()   
            return error