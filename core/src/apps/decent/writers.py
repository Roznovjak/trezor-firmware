from micropython import const

from trezor.messages import (
    DecentAccountOptions,
    DecentAsset,
    DecentAuthority,
    DecentMemo,
    DecentOperationAccountCreate,
    DecentOperationAccountUpdate,
    DecentOperationTransfer,
    DecentTxHeader,
)
from trezor.utils import HashWriter

from apps.common.writers import (
    write_bytes,
    write_uint8,
    write_uint16_le,
    write_uint32_le,
    write_uint64_le,
)

DECENT_OP_ID_ACCOUNT_CREATE = const(1)
DECENT_OP_ID_ACCOUNT_UPDATE = const(2)
DECENT_OP_ID_TRANSFER = const(39)


def write_variant32(w: bytearray, value: int) -> int:
    variant = bytearray()
    while True:
        b = value & 0x7F
        value >>= 7
        b |= (value > 0) << 7
        variant.append(b)

        if value == 0:
            break

    write_bytes(w, bytes(variant))


def write_variant48(w: bytearray, value: int) -> int:
    write_variant32(w, value)


def write_header(hasher: HashWriter, header: DecentTxHeader):
    write_uint16_le(hasher, header.ref_block_num)
    write_uint32_le(hasher, header.ref_block_prefix)
    write_uint32_le(hasher, header.expiration)


def write_asset(w: bytearray, asset: DecentAsset):
    write_uint64_le(w, asset.amount)
    write_variant48(w, asset.asset_id)


def write_memo(w: bytearray, memo: DecentMemo):
    write_bytes(w, memo.sender_pub_key)
    write_bytes(w, memo.receiver_pub_key)
    write_uint64_le(w, memo.nonce)
    write_bytes(w, memo.message)


def write_operation_transfer(w: bytearray, msg: DecentOperationTransfer):
    write_variant32(w, DECENT_OP_ID_TRANSFER)  # operation ID
    write_asset(w, msg.fee)
    write_variant48(w, msg.sender.id)
    write_uint64_le(w, msg.receiver.id)
    write_asset(w, msg.amount)
    write_uint8(w, 1 if msg.memo else 0)
    if msg.memo:
        write_bytes(w, msg.memo.sender_pub_key)
        write_bytes(w, msg.memo.receiver_pub_key)
        write_uint64_le(w, msg.memo.nonce)
        write_variant32(w, len(msg.memo.message))
        write_bytes(w, msg.memo.message)
    write_variant32(w, 0)  # empty op.extension


def write_authority(w: bytearray, auth: DecentAuthority):
    write_uint32_le(w, auth.threshold)
    write_variant32(w, len(auth.accounts))
    for account in auth.accounts:
        write_variant48(w, account.account.id)
        write_uint16_le(w, account.weight)

    write_variant32(w, len(auth.keys))
    for key in auth.keys:
        write_bytes(w, key.key)
        write_uint16_le(w, key.weight)


def write_account_options(w: bytearray, options: DecentAccountOptions):
    write_bytes(w, options.memo_key)
    write_variant48(w, options.voting_account.id)
    write_uint16_le(w, options.num_miner)
    write_variant32(w, len(options.votes))
    for vote in options.votes:
        write_uint32_le(w, vote)
    write_uint8(w, 0)  # empty options.extension
    write_uint8(w, 1 if options.allow_subscription else 0)
    write_asset(w, options.price_per_subscribe)
    write_uint32_le(w, options.subscription_period)


def write_operation_account_create(w: bytearray, msg: DecentOperationAccountCreate):
    write_variant32(w, DECENT_OP_ID_ACCOUNT_CREATE)  # operation ID
    write_asset(w, msg.fee)
    write_variant48(w, msg.registrar.id)
    write_variant32(w, len(msg.name))
    write_bytes(w, msg.name)
    write_authority(w, msg.owner)
    write_authority(w, msg.active)
    write_account_options(w, msg.options)
    write_uint8(w, 0)  # empty op.extension


def write_operation_account_update(w: bytearray, msg: DecentOperationAccountUpdate):
    write_variant32(w, DECENT_OP_ID_ACCOUNT_UPDATE)  # operation ID
    write_asset(w, msg.fee)
    write_variant48(w, msg.account.id)
    write_uint8(w, 1 if msg.owner else 0)
    if msg.owner:
        write_authority(w, msg.owner)
    write_uint8(w, 1 if msg.active else 0)
    if msg.active:
        write_authority(w, msg.active)
    write_uint8(w, 1 if msg.new_options else 0)
    if msg.new_options:
        write_account_options(w, msg.new_options)
    write_uint8(w, 0)  # empty op.extension
