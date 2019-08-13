from micropython import const
from ubinascii import hexlify

from trezor import ui, wire
from trezor.messages import (
    ButtonRequestType,
    DecentOperationAccountCreate,
    DecentOperationAccountUpdate,
    DecentOperationTransfer,
    MessageType,
)
from trezor.messages.ButtonRequest import ButtonRequest
from trezor.ui.confirm import CONFIRMED, ConfirmDialog
from trezor.ui.scroll import Scrollpage, animate_swipe, paginate
from trezor.ui.text import Text
from trezor.utils import chunks

from apps.decent import helpers
from apps.decent.get_public_key import _public_key_to_wif

_LINE_LENGTH = const(17)
_LINE_PLACEHOLDER = "{:<" + str(_LINE_LENGTH) + "}"
_FIRST_PAGE = const(0)
_FOUR_FIELDS_PER_PAGE = const(4)


async def confirm_operation_transfer(ctx, msg: DecentOperationTransfer):
    await ctx.call(
        ButtonRequest(code=ButtonRequestType.ConfirmOutput), MessageType.ButtonAck
    )

    text = "Transfer"
    fields = []
    fields.append("Fee Amount:")
    fields.append(str(msg.fee.amount))
    fields.append("Fee Asset ID:")
    fields.append(helpers.asset_id_to_string(msg.fee.asset_id))
    fields.append("From:")
    fields.append(helpers.account_id_to_string(msg.sender.id))
    fields.append("To:")
    fields.append(helpers.object_id_to_string(msg.receiver))
    fields.append("Amount:")
    fields.append(str(msg.amount.amount))
    fields.append("Asset ID:")
    fields.append(helpers.asset_id_to_string(msg.amount.asset_id))

    if msg.memo:
        fields.append("Memo:")
        fields += split_data(hexlify(msg.memo.message[:512]).decode("ascii"))

    pages = list(chunks(fields, _FOUR_FIELDS_PER_PAGE))

    paginator = paginate(show_lines_page, len(pages), _FIRST_PAGE, pages, text)
    await ctx.wait(paginator)


async def confirm_operation_account_create(ctx, msg: DecentOperationAccountCreate):
    await ctx.call(
        ButtonRequest(code=ButtonRequestType.ConfirmOutput), MessageType.ButtonAck
    )

    text = "New Account"
    fields = []
    fields.append("Fee Amount:")
    fields.append(str(msg.fee.amount))
    fields.append("Fee Asset ID:")
    fields.append(helpers.asset_id_to_string(msg.fee.asset_id))
    fields.append("Creator:")
    fields.append(helpers.account_id_to_string(msg.registrar.id))
    fields.append("Name:")
    fields += split_data(msg.name)
    fields.append("Owner Authority:")
    fields += authorization_fields(msg.owner)
    fields.append("Active Authority:")
    fields += authorization_fields(msg.active)
    fields += account_options_fields(msg.options)

    pages = list(chunks(fields, _FOUR_FIELDS_PER_PAGE))
    paginator = paginate(show_lines_page, len(pages), _FIRST_PAGE, pages, text)

    await ctx.wait(paginator)


async def confirm_operation_account_update(ctx, msg: DecentOperationAccountUpdate):
    await ctx.call(
        ButtonRequest(code=ButtonRequestType.ConfirmOutput), MessageType.ButtonAck
    )

    text = "Update Account"
    fields = []
    fields.append("Fee Amount:")
    fields.append(str(msg.fee.amount))
    fields.append("Fee Asset ID:")
    fields.append(helpers.asset_id_to_string(msg.fee.asset_id))
    fields.append("Account:")
    fields.append(helpers.account_id_to_string(msg.account.id))
    if msg.owner:
        fields.append("Owner Authority:")
        fields += authorization_fields(msg.owner)
    if msg.active:
        fields.append("Active Authority:")
        fields += authorization_fields(msg.active)
    if msg.new_options:
        fields += account_options_fields(msg.new_options)

    pages = list(chunks(fields, _FOUR_FIELDS_PER_PAGE))
    paginator = paginate(show_lines_page, len(pages), _FIRST_PAGE, pages, text)

    await ctx.wait(paginator)


@ui.layout
async def show_lines_page(page: int, page_count: int, pages: list, header: str):
    if header == "Arbitrary data":
        text = Text(header, ui.ICON_WIPE, icon_color=ui.RED)
    else:
        text = Text(header, ui.ICON_CONFIRM, icon_color=ui.GREEN)
    text.mono(*pages[page])

    content = Scrollpage(text, page, page_count)
    if page + 1 == page_count:
        if await ConfirmDialog(content) != CONFIRMED:
            raise wire.ActionCancelled("Action cancelled")
    else:
        content.render()
        await animate_swipe()


def authorization_fields(auth):
    fields = []

    fields.append("Threshold:")
    fields.append(str(auth.threshold))

    for i, key in enumerate(auth.keys):
        _key = _public_key_to_wif(bytes(key.key))
        _weight = str(key.weight)

        header = "Key #{}:".format(i + 1)
        w_header = "Key #{} Weight:".format(i + 1)
        fields.append(header)
        fields += split_data(_key)
        fields.append(w_header)
        fields.append(_weight)

    for i, account in enumerate(auth.accounts):
        _account = helpers.account_id_to_string(account.account.id)

        a_header = "Account #{}:".format(i + 1)
        w_header = "Account #{} weight:".format(i + 1)

        fields.append(a_header)
        fields.append(_account)
        fields.append(w_header)
        fields.append(str(account.weight))

    return fields


def account_options_fields(options):
    fields = []

    fields.append("Memo Key:")
    fields += split_data(_public_key_to_wif(bytes(options.memo_key)))
    fields.append("Voting Account")
    fields.append(helpers.account_id_to_string(options.voting_account.id))
    fields.append("# Of Miners: " + str(options.num_miner))
    if options.votes:
        fields.append("Votes:")
        for vote in options.votes:
            fields.append(helpers.vote_id_to_string(vote))

    return fields


def split_data(data):
    temp_list = []
    len_left = len(data)
    while len_left > 0:
        temp_list.append("{} ".format(data[:_LINE_LENGTH]))
        data = data[_LINE_LENGTH:]
        len_left = len(data)
    return temp_list
