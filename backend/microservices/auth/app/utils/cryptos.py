import secrets
import hashlib
import bcrypt


async def get_email_confirmation_code() -> str:
    code = ""
    for _ in range(6):
        code += str(secrets.randbelow(10))
    return code

async def hash_with_hashlib(data: str) -> str:
    data = data.encode('utf-8')
    hash_obj = hashlib.sha224(data)

    return hash_obj.hexdigest()

def hash_with_bcrypt(data: str) -> str:
    salt = bcrypt.gensalt()
    hashed_data = bcrypt.hashpw(data.encode('utf-8'), salt)
    return hashed_data.decode('utf-8')