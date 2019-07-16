from trezor import wire
from trezor.messages import MessageType

from apps.common import HARDENED

CURVE = "secp256k1"


def boot():
    ns = [[CURVE, HARDENED | 44, HARDENED | 343]]

    wire.add(MessageType.DecentGetPublicKey, __name__, "get_public_key", ns)
    wire.add(MessageType.DecentSignTx, __name__, "sign_tx", ns)
