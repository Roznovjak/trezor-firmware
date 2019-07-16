from trezor import wire
from trezor.crypto.curve import secp256k1
from trezor.crypto.hashlib import sha256
from trezor.messages.DecentSignedTx import DecentSignedTx
from trezor.messages.DecentSignTx import DecentSignTx
from trezor.messages.DecentTxOperationRequest import DecentTxOperationRequest
from trezor.messages.MessageType import DecentTxOperationAck
from trezor.utils import HashWriter

from apps.common import paths
from apps.decent import CURVE, writers
from apps.decent.operations import process_operation
from apps.decent.helpers import validate_full_path
from apps.decent.layout import require_sign_tx

from ubinascii import hexlify


async def sign_tx(ctx, msg: DecentSignTx, keychain):
    if msg.chain_id is None:
        raise wire.DataError("No chain id")
    if msg.header is None:
        raise wire.DataError("No header")
    if msg.num_operations is None or msg.num_operations == 0:
        raise wire.DataError("No operations")

    await paths.validate_path(ctx, validate_full_path, keychain, msg.address_n, CURVE)

    node = keychain.derive(msg.address_n)
    sha = HashWriter(sha256())
    await _init(ctx, sha, msg)
    await _operations(ctx, sha, msg.num_operations)
    writers.write_variant32(sha, 0)  # empty tx.extension
    digest = sha.get_digest()
    signature = secp256k1.sign(
        node.private_key(), digest, True, secp256k1.CANONICAL_SIG_EOS
    )

    return DecentSignedTx(signature=hexlify(signature).decode('ascii'))


async def _init(ctx, sha, msg):
    writers.write_bytes(sha, msg.chain_id)
    writers.write_header(sha, msg.header)
    writers.write_variant32(sha, msg.num_operations)

    await require_sign_tx(ctx, msg.num_operations)


async def _operations(ctx, sha, num_operations: int):
    for i in range(num_operations):
        operation = await ctx.call(DecentTxOperationRequest(), DecentTxOperationAck)
        await process_operation(ctx, sha, operation)
