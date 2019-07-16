# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

from .DecentOperationAccountCreate import DecentOperationAccountCreate
from .DecentOperationAccountUpdate import DecentOperationAccountUpdate
from .DecentOperationTransfer import DecentOperationTransfer


class DecentTxOperationAck(p.MessageType):
    MESSAGE_WIRE_TYPE = 654

    def __init__(
        self,
        operation_id: int = None,
        transfer: DecentOperationTransfer = None,
        account_update: DecentOperationAccountUpdate = None,
        account_create: DecentOperationAccountCreate = None,
    ) -> None:
        self.operation_id = operation_id
        self.transfer = transfer
        self.account_update = account_update
        self.account_create = account_create

    @classmethod
    def get_fields(cls):
        return {
            1: ('operation_id', p.UVarintType, 0),
            2: ('transfer', DecentOperationTransfer, 0),
            3: ('account_update', DecentOperationAccountUpdate, 0),
            4: ('account_create', DecentOperationAccountCreate, 0),
        }
