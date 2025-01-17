# Automatically generated by pb2py
# fmt: off
import protobuf as p


class DecentPublicKey(p.MessageType):
    MESSAGE_WIRE_TYPE = 651

    def __init__(
        self,
        wif_public_key: str = None,
        raw_public_key: bytes = None,
    ) -> None:
        self.wif_public_key = wif_public_key
        self.raw_public_key = raw_public_key

    @classmethod
    def get_fields(cls):
        return {
            1: ('wif_public_key', p.UnicodeType, 0),
            2: ('raw_public_key', p.BytesType, 0),
        }
