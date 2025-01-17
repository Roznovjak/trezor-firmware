# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

from .DecentAccountId import DecentAccountId
from .DecentAsset import DecentAsset
from .DecentMemo import DecentMemo
from .DecentObjectId import DecentObjectId


class DecentOperationTransfer(p.MessageType):

    def __init__(
        self,
        fee: DecentAsset = None,
        sender: DecentAccountId = None,
        receiver: DecentObjectId = None,
        amount: DecentAsset = None,
        memo: DecentMemo = None,
    ) -> None:
        self.fee = fee
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.memo = memo

    @classmethod
    def get_fields(cls):
        return {
            1: ('fee', DecentAsset, 0),
            2: ('sender', DecentAccountId, 0),
            3: ('receiver', DecentObjectId, 0),
            4: ('amount', DecentAsset, 0),
            5: ('memo', DecentMemo, 0),
        }
