import pytest

from trezorlib.decent import get_public_key
from trezorlib.tools import parse_path

from .common import TrezorTest


@pytest.mark.skip_t1
@pytest.mark.decent
class TestMsgDecentGetpublickey(TrezorTest):
    def test_decent_get_public_key(self):
        self.setup_mnemonic_nopin_nopassphrase()
        public_key = get_public_key(self.client, parse_path("m/44'/343'/0'/0/0"))
        assert (
            public_key.wif_public_key
            == "DCT7qd59RnZtJC7d6cFvXYnFmdjtBJkg2DxizoSYVcJgexvUk9GFA"
        )
        assert (
            public_key.raw_public_key.hex()
            == "0384941eb6c4c8d807dffbeb12daedc31de36d2db8e0f305843e2bb835d9ee1e1f"
        )
        public_key = get_public_key(self.client, parse_path("m/44'/343'/0'/0/1"))
        assert (
            public_key.wif_public_key
            == "DCT6kiy7aHbjNwxeFmkVN8r1KyCgNxaAXYr9uaEPHmvwuZNuhnodJ"
        )
        assert (
            public_key.raw_public_key.hex()
            == "02f5c29cf093ccef4208acebed75f5d910de5e8ecb6470722f8e33fc94d017e1bb"
        )
        public_key = get_public_key(self.client, parse_path("m/44'/343'/1'/0/0"))
        assert (
            public_key.wif_public_key
            == "DCT5AwThJeTVVkGtY8Y7t7afpppz1HkvLR64omEBXkQBKbXn1f1kp"
        )
        assert (
            public_key.raw_public_key.hex()
            == "02255a1e886526654d43a81ffa09c670829882dc1b72271df511acd5c81c087248"
        )
