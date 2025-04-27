
## Built-in modules: ##
from typing import Optional, Awaitable, Any
from base64 import b64decode, b64encode

## Third-party modules: ##
from Crypto.Cipher import AES, _mode_cbc
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from uuid import uuid4
from uuid import UUID

## Local modules: ##
from core.api_v1.keys.sym_keys.schemas import SymmetricKey
from core.api_v1.sign_up.schemas import UserEncryptedRegistrationModel
from core.async_databases.async_redis import sym_key_redis


async def save_symmetric_key_to_redis(
    symmetric_key_id: UUID,
    key_data_bytes: dict[str, bytes]
) -> Awaitable[None]:
    """Save the symmetric CBC key bytes in redis database. 

    Args:
        data_to_save (dict[str, bytes]): symmetric keys bytes (key and IV)
    """
    async with sym_key_redis.client() as connection:
        await connection.hset(str(symmetric_key_id), mapping=key_data_bytes)


def create_symmetric_key_dependency(
    key_lenght: Optional[int] = 32,
) -> SymmetricKey:
    """Create two asymmetric keys for data encryption.

    Args:
        key_lenght (int): key lenght in bytes.

    Returns:
        SymmetricKey: private and public keys.
    """
    ## IV must be 16 bytes long. ##
    IV_LENGHT: int = 16
    sym_key: bytes = get_random_bytes(key_lenght)
    iv: bytes = get_random_bytes(IV_LENGHT)   
    key_id: UUID = uuid4() 
    
    return SymmetricKey(
        key_id=key_id,
        sym_key=sym_key,
        key_iv=iv,
    )


def get_sym_key_cipher(
    sym_key: bytes,
    iv: bytes,
) -> _mode_cbc.CbcMode:
    """Get cipher object for symmetric key.

    Args:
        sym_key (bytes): symmetric key bytes.
        iv (bytes): initialization vector bytes.

    Returns:
        _mode_cbc.CbcMode: Cipher object.
    """
    return AES.new(
        key=sym_key,
        mode=AES.MODE_CBC,
        iv=iv
    )


class AESDataEncrypter:
    """Class to encrypt data with symmetric key and encode the cipher by base64."""
    def __init__(
        self,
        data_to_encrypt: str | bytes,
        symmetric_key: SymmetricKey,
        encode_data_to_base64: Optional[bool] = False,
    ) -> None:
        """Checks the data_to_encrypt type, and encrypt it.
        Automaticly encode encrypted data to base64 if you set it _summary_in initialization.

        Args:
            data_to_encrypt (str | bytes)
            symmetric_key (SymmetricKey): Symmetric AES key with 16 bytes of IV.
            encode_data_to_base64: Optional[bool]. Encoded encrypted data to base64 or not. Defaults to False.
        """
        self.data_to_encrypt: bytes = self._check_data_to_encrypt_type(
            data_to_encrypt=data_to_encrypt
        )
        self.symmetric_key: SymmetricKey = symmetric_key
        self.encrypted_data: bytes = self._encrypt_data_by_sym_key()
        if encode_data_to_base64:
            self.encode_data_to_base64()
    
    def encode_data_to_base64(self) -> None:
        """Encode the encrypted data to base64.
        Use after data encrypting."""
        self.encrypted_data: bytes = b64encode(self.encrypted_data)

    def _encrypt_data_by_sym_key(self) -> bytes:
        """Encypt data by symmetric key cipher.

        Args:
            sym_key (_mode_cbc.CbcMode): AES symmetric key with IV. You can get it by AES.new()

        Returns:
            bytes: Encrypted data.
        """
        cipher: _mode_cbc.CbcMode = self._get_cipher_for_key()
        
        return cipher.encrypt(
            pad(
                data_to_pad=self.data_to_encrypt,
                block_size=AES.block_size,
                )
            )
    
    def _get_cipher_for_key(self) -> _mode_cbc.CbcMode:
        """Gets cipher to encode the data.

        Returns:
            _mode_cbc.CbcMode: Cipher.
        """
        cipher: _mode_cbc.CbcMode = get_sym_key_cipher(
            sym_key=self.symmetric_key.sym_key,
            iv=self.symmetric_key.key_iv,
        )
        return cipher
    
    def _check_data_to_encrypt_type(
        self,
        data_to_encrypt: str | bytes,
    ) -> bytes:
        """Checks the type of data_to_encrypt and make it bytes if it isn't.

        Args:
            data_to_encrypt (str | bytes)

        Returns:
            bytes: bytes of data_to_encrypt.
        """
        if isinstance(data_to_encrypt, str):
            data_to_encrypt: bytes = data_to_encrypt.encode()
        
        return data_to_encrypt


class AESDataDecrypter():
    """Class to decrypt encrypted data by AES"""
    def __init__(
        self,
        data_to_decrypt: bytes,
        symmetric_key: SymmetricKey,
        decode_data_from_base64: Optional[bool] = False,
    ) -> None:
        """Decode the data from base64 if you set it. Decrypt the encrypted data by AES key.

        Args:
            data_to_decrypt (bytes): Encrypted by the same key data.
            symmetric_key (SymmetricKey): Key, that used to encrypt the data
            decode_data_from_base64 (Optional[bool], optional): Decode the data from base64 or not. Defaults to False.
        """
        self.data_to_decrypt: bytes = data_to_decrypt
        if decode_data_from_base64:
            self.decode_data_from_base64()
        self.symmetric_key: SymmetricKey = symmetric_key
        self.decrypted_data: Any = self._decrypt_data_by_sym_key()
    
    def decode_data_from_base64(self) -> None:
        """Decode the current encoded data from base64."""
        self.data_to_decrypt: bytes = b64decode(self.data_to_decrypt)

    def _get_cipher_for_key(self) -> _mode_cbc.CbcMode:
        """Gets cipher to encode the data.

        Returns:
            _mode_cbc.CbcMode: Cipher.
        """
        cipher: _mode_cbc.CbcMode = get_sym_key_cipher(
            sym_key=self.symmetric_key.sym_key,
            iv=self.symmetric_key.key_iv,
        )
        return cipher

    def _decrypt_data_by_sym_key(self) -> Any:
        """Decrypt data by the symmetric key.

        Args:
            private_key (str),
            data_to_decode (bytes).
            decode_base64 (bool). Option to decode the data by bas64 of not. Default to True.

        Returns:
            bytes: Decoded data.
        """
        cipher: _mode_cbc.CbcMode = self._get_cipher_for_key()
        
        decoded_data: Any = unpad(
            cipher.decrypt(self.data_to_decrypt),
            AES.block_size
        )
        return decoded_data


def decrypt_user_data_by_sym_key(
    user_data: UserEncryptedRegistrationModel,
    symmetric_key: SymmetricKey
) -> tuple[bytes]:
    """Decrypt the user data.

    Args:
        user_data (UserEncryptedRegistrationModel): Encrypted model with login and password.
        symmetric_key (SymmetricKey): symmetric key model.

    Returns:
        tuple[bytes]: _description_
    """
    user_login: bytes = AESDataDecrypter(
        data_to_decrypt=user_data.encrypted_login,
        symmetric_key=symmetric_key,
        decode_data_from_base64=True,
    ).decrypted_data
    user_password: bytes = AESDataDecrypter(
        data_to_decrypt=user_data.encrypted_password,
        symmetric_key=symmetric_key,
        decode_data_from_base64=True,
    ).decrypted_data
    
    return (user_login, user_password)


async def get_symmetric_key_from_redis(key_id: str) -> Awaitable[SymmetricKey]:
    """Get the Symmetric key from Redis database.

    Args:
        key_id (str): symmetric key id.

    Returns:
        SymmetricKey: Key object with the key_id, sym_key and key_iv.
    """
    async with sym_key_redis.client() as connection:
        sym_key_hash = await connection.hgetall(key_id)
    
    sym_key = sym_key_hash.get(b'sym_key')
    key_iv = sym_key_hash.get(b'key_iv')
    
    return SymmetricKey(
        key_id=key_id,
        sym_key=sym_key,
        key_iv=key_iv,
    )