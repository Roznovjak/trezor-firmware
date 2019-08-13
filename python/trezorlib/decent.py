from datetime import datetime

from . import messages
from .tools import CallException, b58decode, expect, session

# Operation types
CREATE_ACCOUNT_OP_ID = 1
UPDATE_ACCOUNT_OP_ID = 2
TRANSFER_OP_ID = 39


def parse_id(object_num: str):
    split = object_num.split(".", maxsplit=2)
    return int(split[2])


def parse_object_id(object_num: str):
    object_space, object_type, object_id = object_num.split(".", maxsplit=2)
    result = (int(object_space) << 56) | (int(object_type) << 48) | int(object_id)
    return messages.DecentObjectId(result)


def parse_asset(asset):
    return messages.DecentAsset(
        amount=int(asset["amount"]), asset_id=parse_id(asset["asset_id"])
    )


def public_key_to_buffer(pub_key):
    return b58decode(pub_key[3:], None)[:-4]


def parse_transfer(data):
    fee = parse_asset(data["fee"])
    sender = messages.DecentAccountId(parse_id(data["from"]))
    receiver = parse_object_id(data["to"])
    amount = parse_asset(data["amount"])

    memo = None
    memo_data = data.get("memo")
    if memo_data:
        memo_from = public_key_to_buffer(memo_data["from"])
        memo_to = public_key_to_buffer(memo_data["to"])
        memo_nonce = int(memo_data["nonce"])
        memo_msg = bytes.fromhex(memo_data["message"])
        memo = messages.DecentMemo(memo_from, memo_to, memo_nonce, memo_msg)

    return messages.DecentOperationTransfer(fee, sender, receiver, amount, memo)


def parse_authority(data):
    accounts = []
    for item in data["account_auths"]:
        account, weight = item
        accounts.append(
            messages.DecentAuthorityAccount(
                account=messages.DecentAccountId(parse_id(account)), weight=int(weight)
            )
        )

    keys = []
    for item in data["key_auths"]:
        key, weight = item
        keys.append(
            messages.DecentAuthorityKey(
                key=public_key_to_buffer(key), weight=int(weight)
            )
        )

    return messages.DecentAuthority(
        threshold=int(data["weight_threshold"]), accounts=accounts, keys=keys
    )


def parse_vote(vote: str):
    vote_type, vote_instance = vote.split(":")
    return int(vote_instance) << 8 | int(vote_type)


def parse_account_options(data):
    memo = public_key_to_buffer(data["memo_key"])
    voting_account = messages.DecentAccountId(parse_id(data["voting_account"]))
    num_miner = int(data["num_miner"])
    votes = []
    for vote in data["votes"]:
        votes.append(parse_vote(vote))
    allow_subscription = data["allow_subscription"]
    price_per_subscribe = parse_asset(data["price_per_subscribe"])
    subscription_period = int(data["subscription_period"])

    return messages.DecentAccountOptions(
        memo,
        voting_account,
        num_miner,
        votes,
        allow_subscription,
        price_per_subscribe,
        subscription_period,
    )


def parse_account_create(data):
    fee = parse_asset(data["fee"])
    registrar = messages.DecentAccountId(parse_id(data["registrar"]))
    name = data["name"]
    owner = parse_authority(data["owner"])
    active = parse_authority(data["active"])
    options = parse_account_options(data["options"])

    return messages.DecentOperationAccountCreate(
        fee, registrar, name, owner, active, options
    )


def parse_account_update(data):
    fee = parse_asset(data["fee"])
    account = messages.DecentAccountId(parse_id(data["account"]))
    owner = None
    if data.get("owner"):
        owner = parse_authority(data["owner"])

    active = None
    if data.get("active"):
        active = parse_authority(data["active"])

    new_options = None
    if data.get("new_options"):
        new_options = parse_account_options(data["new_options"])

    return messages.DecentOperationAccountUpdate(
        fee, account, owner, active, new_options
    )


def parse_operation(operation):
    tx_operation = messages.DecentTxOperationAck()
    operation_id, data = operation[:2]

    tx_operation.operation_id = operation_id

    if operation_id == TRANSFER_OP_ID:
        tx_operation.transfer = parse_transfer(data)
    elif operation_id == CREATE_ACCOUNT_OP_ID:
        tx_operation.account_create = parse_account_create(data)
    elif operation_id == UPDATE_ACCOUNT_OP_ID:
        tx_operation.account_update = parse_account_update(data)
    else:
        raise ValueError("Unsupported operation type: " + str(operation_id))

    return tx_operation


def parse_transaction_json(transaction):
    header = messages.DecentTxHeader()
    header.ref_block_num = int(transaction["ref_block_num"])
    header.ref_block_prefix = int(transaction["ref_block_prefix"])
    header.expiration = int(
        (
            datetime.strptime(transaction["expiration"], "%Y-%m-%dT%H:%M:%S")
            - datetime(1970, 1, 1)
        ).total_seconds()
    )

    operations = [parse_operation(a) for a in transaction["operations"]]

    return header, operations


# ====== Client functions ====== #


@expect(messages.DecentPublicKey)
def get_public_key(client, n, show_display=False):
    response = client.call(
        messages.DecentGetPublicKey(address_n=n, show_display=show_display)
    )
    return response


@session
def sign_tx(client, address, transaction, chain_id):
    header, operations = parse_transaction_json(transaction)

    msg = messages.DecentSignTx()
    msg.address_n = address
    msg.chain_id = bytes.fromhex(chain_id)
    msg.header = header
    msg.num_operations = len(operations)

    response = client.call(msg)

    try:
        while isinstance(response, messages.DecentTxOperationRequest):
            response = client.call(operations.pop(0))
    except IndexError:
        # pop from empty list
        raise CallException(
            "Decent.UnexpectedEndOfOperations",
            "Reached end of operations without a signature.",
        ) from None

    if not isinstance(response, messages.DecentSignedTx):
        raise CallException(messages.FailureType.UnexpectedMessage, response)

    return response
