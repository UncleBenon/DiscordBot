from hashlib import sha256
from time import time

def getSha256(items) -> str:

    out = sha256()

    if isinstance(items, list) or isinstance(items, tuple):
        for i in items:
            out.update(
                str(i).encode()
            )
    else:
        out.update(
            str(items).encode()
        )

    out.update(str(time()).encode())
    return out.hexdigest()
