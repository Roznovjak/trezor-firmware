from common import *

from apps.decent.writers import (DECENT_OP_ID_ACCOUNT_CREATE,
                                 DECENT_OP_ID_ACCOUNT_UPDATE,
                                 DECENT_OP_ID_TRANSFER,
                                 )
from apps.decent.operations import check_operation
from trezor.messages.DecentTxOperationAck import DecentTxOperationAck
from trezor.messages.DecentOperationTransfer import DecentOperationTransfer
from trezor.messages.DecentOperationAccountCreate import DecentOperationAccountCreate
from trezor.messages.DecentOperationAccountUpdate import DecentOperationAccountUpdate


class TestDecentOperations(unittest.TestCase):
    def test_check_action(self):
        # return True
        self.assertEqual(check_operation(DecentTxOperationAck(transfer=DecentOperationTransfer(),
                                                              operation_id=DECENT_OP_ID_TRANSFER)),
                         True)
        self.assertEqual(check_operation(DecentTxOperationAck(account_create=DecentOperationAccountCreate(),
                                                              operation_id=DECENT_OP_ID_ACCOUNT_CREATE)),
                         True)
        self.assertEqual(check_operation(DecentTxOperationAck(account_update=DecentOperationAccountUpdate(),
                                                              operation_id=DECENT_OP_ID_ACCOUNT_UPDATE)),
                         True)

        # returns False
        self.assertEqual(check_operation(DecentTxOperationAck()), False)
        self.assertEqual(check_operation(DecentTxOperationAck(transfer=DecentOperationTransfer())),
                         False)
        self.assertEqual(check_operation(DecentTxOperationAck(transfer=DecentOperationTransfer(),
                                                              operation_id=DECENT_OP_ID_ACCOUNT_CREATE)),
                         False)
        self.assertEqual(check_operation(DecentTxOperationAck(account_create=DecentOperationAccountCreate(),
                                                              operation_id=DECENT_OP_ID_TRANSFER)),
                         False)
        self.assertEqual(check_operation(DecentTxOperationAck(account_update=DecentOperationAccountUpdate(),
                                                              operation_id=DECENT_OP_ID_ACCOUNT_CREATE)),
                         False)
        self.assertEqual(check_operation(DecentTxOperationAck(account_update=DecentOperationAccountUpdate(),
                                                              operation_id=0)),
                         False)


if __name__ == '__main__':
    unittest.main()
