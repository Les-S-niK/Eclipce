
## Built-in modules: ##
from os import remove, PathLike, mkdir
from os.path import join, exists
from typing import Awaitable
import aiofiles

## Third-party modules: ##
from gnupg import GPG, Crypt
from core.api_v1.keys.sym_keys.schemas import SymmetricKey
from uuid import UUID

## Local modules: ##
from .gnupg_config import KEYS_STORE_PATH, GNUPG_ACTIONS_OPTIONS, GNUPG_OPTIONS


FILE_EXST: str = ".aes"
gpg: GPG = GPG(
    gpgbinary="/usr/bin/gpg",
    gnupghome=KEYS_STORE_PATH,
    options=GNUPG_OPTIONS
)


class GnupgFolderManager:
    """Class to manage files in secure directory with AES keys."""
    def __init__(
        self,
        symmetric_key_id: UUID,
    ) -> None:
        if not exists(KEYS_STORE_PATH):
            mkdir(KEYS_STORE_PATH)
        self.file_path: PathLike = join(KEYS_STORE_PATH, f"{symmetric_key_id}{FILE_EXST}")
    
    async def get_key_from_file(self) -> Awaitable[bytes | None]:
        """Read the file and return readed key.

        Returns:
            bytes | None: readed encrypted key. None if file doesn't exists.
        """
        try:
            async with aiofiles.open(
                file=self.file_path,
                mode="rb"
            ) as file:
                readed: bytes = await file.read()
        except FileNotFoundError:
            readed = None
        
        return readed

    async def write_key_in_file(
        self,
        encrypted_symmetric_key: bytes
    ) -> Awaitable[None]:
        """Write the GNUPG encrypted key in file.

        Args:
            encrypted_symmetric_key (bytes): Bytes of the encrypted AES key by GNUPG.
        """
        async with aiofiles.open(
            file=self.file_path,
            mode="wb"
        ) as file:
            await file.write(encrypted_symmetric_key)
    
    def remove_file(self) -> None:
        """Remove the file with AES encrypted key from folder."""
        try:
            remove(self.file_path)
        except FileNotFoundError:
            pass


def gnupg_encrypt_key(
    symmetric_key: SymmetricKey,
    ) -> bytes:
    """Encrypt the symmetric key by GNUPG AES and return encrypted model.

    Args:
        symmetric_key (SymmetricKey): Symmetric key to encrypt.
        options (GnupgActionsOptions): Encrypting options.

    Returns:
        bytes: Encrypted by AES symmetric key. 
    """
    data_to_save: bytes = symmetric_key.sym_key + symmetric_key.key_iv
    encypted_symmetric_key: Crypt = gpg.encrypt(
        data=data_to_save,
        recipients=None,
        **GNUPG_ACTIONS_OPTIONS.__dict__
    )
    return encypted_symmetric_key.data


def gnupg_decrypt_key(
    symmetric_key_id: UUID,
    encrypted_symmetric_key: bytes,
) -> SymmetricKey:
    """Decrypt the encrypted symmetric key by GNUPG AES and return decrypted model.

    Args:
        encrypted_symmetric_key (EncryptedSymmetricKey): Encrypted symmetric key to decrypt.
        options (GnupgActionsOptions): Encrypting options.

    Returns:
        SymmetricKey: Decrypted by AES symmetric key. 
    """
    decrypted_symmetric_key_data: bytes = gpg.decrypt(
        message=encrypted_symmetric_key,
        **GNUPG_ACTIONS_OPTIONS.__dict__
    )
    decrypted_symmetric_key: SymmetricKey = SymmetricKey(
        key_id=symmetric_key_id,
        sym_key=decrypted_symmetric_key_data[:32],
        key_iv=decrypted_symmetric_key_data[32:48]
    )
    return decrypted_symmetric_key