# Automatically generated by pb2py
# fmt: off
import protobuf as p

from .DecentOperationCreateAccount import DecentOperationCreateAccount
from .DecentOperationTransfer import DecentOperationTransfer
from .DecentOperationUnknown import DecentOperationUnknown
from .DecentOperationUpdateAccount import DecentOperationUpdateAccount


class DecentTxOperationAck(p.MessageType):
    MESSAGE_WIRE_TYPE = 654

    def __init__(
        self,
        transfer: DecentOperationTransfer = None,
        update_account: DecentOperationUpdateAccount = None,
        create_account: DecentOperationCreateAccount = None,
        unknown: DecentOperationUnknown = None,
    ) -> None:
        self.transfer = transfer
        self.update_account = update_account
        self.create_account = create_account
        self.unknown = unknown

    @classmethod
    def get_fields(cls):
        return {
            1: ('transfer', DecentOperationTransfer, 0),
            2: ('update_account', DecentOperationUpdateAccount, 0),
            3: ('create_account', DecentOperationCreateAccount, 0),
            4: ('unknown', DecentOperationUnknown, 0),
        }
