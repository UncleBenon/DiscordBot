def getSha256(items) -> str:
    from hashlib import sha256
    from time import time

    out = sha256()

    if isinstance(items, list) or isinstance(items, list):
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

if __name__ == "__main__":
    print(
        getSha256(("test", "lmao"))
    )
