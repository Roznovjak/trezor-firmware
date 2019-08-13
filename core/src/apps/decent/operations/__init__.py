from trezor.messages.MessageType import DecentTxOperationAck

from apps.decent import writers
from apps.decent.operations import layout


async def process_operation(ctx, sha, operation: DecentTxOperationAck):

    if not check_operation(operation):
        raise ValueError("Invalid action")

    w = bytearray()
    if operation.operation_id == writers.DECENT_OP_ID_TRANSFER:
        await layout.confirm_operation_transfer(ctx, operation.transfer)
        writers.write_operation_transfer(w, operation.transfer)
    elif operation.operation_id == writers.DECENT_OP_ID_ACCOUNT_CREATE:
        await layout.confirm_operation_account_create(ctx, operation.account_create)
        writers.write_operation_account_create(w, operation.account_create)
    elif operation.operation_id == writers.DECENT_OP_ID_ACCOUNT_UPDATE:
        await layout.confirm_operation_account_update(ctx, operation.account_update)
        writers.write_operation_account_update(w, operation.account_update)
    else:
        raise ValueError("Unsupported operation type: " + str(operation.operation_id))

    writers.write_bytes(sha, w)


def check_operation(operation: DecentTxOperationAck):
    if (
        (
            operation.operation_id == writers.DECENT_OP_ID_TRANSFER
            and operation.transfer is not None
        )
        or (
            operation.operation_id == writers.DECENT_OP_ID_ACCOUNT_CREATE
            and operation.account_create is not None
        )
        or (
            operation.operation_id == writers.DECENT_OP_ID_ACCOUNT_UPDATE
            and operation.account_update is not None
        )
    ):
        return True
    else:
        return False
