# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

from .DecentAsset import DecentAsset


class DecentOperationTransfer(p.MessageType):

    def __init__(
        self,
        sender: str = None,
        receiver: str = None,
        quantity: DecentAsset = None,
        memo: str = None,
    ) -> None:
        self.sender = sender
        self.receiver = receiver
        self.quantity = quantity
        self.memo = memo

    @classmethod
    def get_fields(cls):
        return {
            1: ('sender', p.UnicodeType, 0),
            2: ('receiver', p.UnicodeType, 0),
            3: ('quantity', DecentAsset, 0),
            4: ('memo', p.UnicodeType, 0),
        }
