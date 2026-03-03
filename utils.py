# utils.py
BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode_base62(num: int) -> str:
    """Convert integer to Base62 string"""
    if num == 0:
        return BASE62[0]
    result = []
    while num > 0:
        num, rem = divmod(num, 62)
        result.append(BASE62[rem])
    return ''.join(reversed(result))

