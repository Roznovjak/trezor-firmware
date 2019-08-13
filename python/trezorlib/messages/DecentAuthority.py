# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

from .DecentAuthorityAccount import DecentAuthorityAccount
from .DecentAuthorityKey import DecentAuthorityKey

if __debug__:
    try:
        from typing import List
    except ImportError:
        List = None  # type: ignore


class DecentAuthority(p.MessageType):

    def __init__(
        self,
        threshold: int = None,
        accounts: List[DecentAuthorityAccount] = None,
        keys: List[DecentAuthorityKey] = None,
    ) -> None:
        self.threshold = threshold
        self.accounts = accounts if accounts is not None else []
        self.keys = keys if keys is not None else []

    @classmethod
    def get_fields(cls):
        return {
            1: ('threshold', p.UVarintType, 0),
            2: ('accounts', DecentAuthorityAccount, p.FLAG_REPEATED),
            3: ('keys', DecentAuthorityKey, p.FLAG_REPEATED),
        }