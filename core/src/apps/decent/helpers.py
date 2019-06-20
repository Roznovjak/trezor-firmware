from trezor.crypto import base58

from apps.common import HARDENED


def base58_encode(prefix: str, sig_prefix: str, data: bytes) -> str:
    b58 = base58.encode(data + base58.ripemd160_32(data + sig_prefix.encode()))
    if sig_prefix:
        return prefix + sig_prefix + "_" + b58
    else:
        return prefix + b58


def validate_full_path(path: list) -> bool:
    """
    Validates derivation path to equal 44'/343'/a'/0/0,
    where `a` is an account index from 0 to 1 000 000.
    Similar to Ethereum this should be 44'/343'/a', but for
    compatibility with other HW vendors we use 44'/343'/a'/0/0.
    """
    if len(path) != 5:
        return False
    if path[0] != 44 | HARDENED:
        return False
    if path[1] != 343 | HARDENED:
        return False
    if path[2] < HARDENED or path[2] > 1000000 | HARDENED:
        return False
    if path[3] != 0:
        return False
    if path[4] != 0:
        return False
    return True
