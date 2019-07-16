from trezor.crypto import base58
from trezor.messages import DecentObjectId

from apps.common import HARDENED


def base58_encode(prefix: str, data: bytes) -> str:
    b58 = base58.encode(data + base58.ripemd160_32(data))
    return prefix + b58


def account_id_to_string(id) -> str:
    return "1.2." + str(id)


def object_id_to_string(id: DecentObjectId) -> str:
    object_space = id.id >> 56
    object_type = id.id >> 48 & 0x00ff
    object_id = id.id & 0xffffffffffff
    return ".".join([str(object_space), str(object_type), str(object_id)])


def asset_id_to_string(asset_id) -> str:
    return "1.3." + str(asset_id)


def vote_id_to_string(vote_id) -> str:
    vote_type = vote_id & 0xff
    vote_instance = vote_id >> 8
    return str(vote_type) + ":" + str(vote_instance)


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
