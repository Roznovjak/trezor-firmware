# Automatically generated by pb2py
# fmt: off
import protobuf as p


class DecentAsset(p.MessageType):

    def __init__(
        self,
        amount: int = None,
        asset_id: int = None,
    ) -> None:
        self.amount = amount
        self.asset_id = asset_id

    @classmethod
    def get_fields(cls):
        return {
            1: ('amount', p.SVarintType, 0),
            2: ('asset_id', p.UVarintType, 0),
        }
