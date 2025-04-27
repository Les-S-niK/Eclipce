
## Built-in modules: ##
from typing import Optional, Any, Generator
from os import getenv, PathLike
from os.path import join

## Local modules: ##
from config import PROJECT_PATH


GNUPG_PATH: PathLike = join(PROJECT_PATH, "core", "gnupg")
KEYS_STORE_PATH: PathLike = join(GNUPG_PATH, "store")


GNUPG_OPTIONS: list[str] = [
    '--armor'
]

class GnupgActionsOptions:
    """Create options for GNUPG acitons."""
    def __init__(
        self,
        passphrase: str,
        symmetric: Optional[str] = "AES256",
        armor: Optional[bool] = True,
    ) -> None:
        """Set the necessary options for Gnupg actions.

        Args:
            passphrase (str): It may be a very strong password (>20 symb with @#%+$%^& etc.)
            symmetric (Optional[str], optional): Type of symmetric encryption. Defaults to "AES256".
            armor (Optional[bool], optional): In default case save the text data . Defaults to True.
        """
        self.passphrase: str = passphrase 
        self.symmetric: str = symmetric
        self.armor: bool = armor
    
    def __iter__(self) -> Generator[None, None, Any]:
        """Make object iterable to unpack it's field if needed. 

        Yields:
            Generator[None, None, Any]: Object unpacked fields with given in initialization values. 
        """
        yield from self.__dict__.values()


GNUPG_ACTIONS_OPTIONS: GnupgActionsOptions = GnupgActionsOptions(
    passphrase=getenv("PASSPHRASE")
)