import hashlib
import os


# ==========================================
# PASSWORD HASHING (salted PBKDF2)
# ==========================================
#
# Stored format: "<salt_hex>$<hash_hex>"
# Using PBKDF2-HMAC-SHA256 with 100,000 iterations — far stronger than a
# bare hashlib.sha256(password) call, while still needing zero extra
# dependencies beyond the standard library.

_ITERATIONS = 100_000


def hash_password(password: str) -> str:
    """Returns a salted PBKDF2 hash string safe to store in the database."""

    salt = os.urandom(16)

    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        _ITERATIONS
    )

    return salt.hex() + "$" + derived.hex()


def verify_password(password: str, stored_hash: str) -> bool:
    """Checks a plain-text password against a stored salt$hash string."""

    try:
        salt_hex, hash_hex = stored_hash.split("$")
    except ValueError:
        return False

    salt = bytes.fromhex(salt_hex)

    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        _ITERATIONS
    )

    return derived.hex() == hash_hex
