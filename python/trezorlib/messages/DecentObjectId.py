# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p


class DecentObjectId(p.MessageType):

    def __init__(
        self,
        id: int = None,
    ) -> None:
        self.id = id

    @classmethod
    def get_fields(cls):
        return {
            1: ('id', p.UVarintType, 0),
        }
