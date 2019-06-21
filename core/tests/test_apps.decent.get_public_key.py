from common import *

from apps.decent.get_public_key import _get_public_key, _public_key_to_wif
from trezor.crypto import bip32, bip39
from ubinascii import hexlify, unhexlify
from apps.common.paths import HARDENED
from apps.decent.helpers import validate_full_path


class TestDecentGetPublicKey(unittest.TestCase):
    def test_get_public_key_scheme(self):
        mnemonic = "zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong"
        seed = bip39.seed(mnemonic, '')

        derivation_paths = [
            [0x80000000 | 44, 0x80000000 | 343, 0x80000000, 0, 0],
            [0x80000000 | 44, 0x80000000 | 343, 0x80000000, 0, 1],
            [0x80000000 | 44, 0x80000000 | 343],
            [0x80000000 | 44, 0x80000000 | 343, 0x80000000, 0, 0x80000000],
        ]

        public_keys = [
            b'03e167cfb66e617f9a6f6798b7d0f9bb6367b5aceeaaf94d0a6d164f64e10949ac',
            b'0226e7bfa10257a7709380570782229c9670c3dd3cbc8e51c9556dfa7e1e5ef980',
            b'03cd4cf716920d6cf95c6ddaa6e79df4c54f3b53737a9bcafda0c176a82cc887cc',
            b'02a0a16ceadda4f66ad947b8dc6308f689bb0c1970728e8a0fc8f705dfaef3bbfc',
        ]

        wif_keys = [
            'DCT8YWDDGXTbQDM6ZbAAe4rKMAbcpuYJeKLc6PERHX7VmaKDzPZP6',
            'DCT5Bd8sQHZCnQ1hj98w9cbzvoLVL5Vj3d3ZciJJnLz4KuLhbUZY3',
            'DCT8PefCnXumV6tPdoYhWVqW7EB7RLeBPCi2kx5CFPRB4usLYCgc3',
            'DCT67ESpK9BaFXzfhUs8ntWUPzNE2yLJcFy6ZcdwNczwDnKJqx1zv',
        ]

        for index, path in enumerate(derivation_paths):
            node = bip32.from_seed(seed, 'secp256k1')
            node.derive_path(path)
            wif, public_key = _get_public_key(node)

            self.assertEqual(hexlify(public_key), public_keys[index])
            self.assertEqual(wif, wif_keys[index])
            self.assertEqual(_public_key_to_wif(public_key), wif_keys[index])

    def test_paths(self):
        # 44'/343'/a'/0/0 is correct
        incorrect_paths = [
            [44 | HARDENED],
            [44 | HARDENED, 343 | HARDENED],
            [44 | HARDENED, 343 | HARDENED, 0 | HARDENED, 0, 0, 0],
            [44 | HARDENED, 343 | HARDENED, 0 | HARDENED, 0 | HARDENED],
            [44 | HARDENED, 343 | HARDENED, 0 | HARDENED, 0 | HARDENED, 0 | HARDENED],
            [44 | HARDENED, 343 | HARDENED, 0 | HARDENED, 1, 0],
            [44 | HARDENED, 343 | HARDENED, 0 | HARDENED, 0, 1],
            [44 | HARDENED, 342 | HARDENED, 0 | HARDENED, 0, 0],
            [44 | HARDENED, 344 | HARDENED, 0 | HARDENED, 0, 9999],
        ]
        correct_paths = [
            [44 | HARDENED, 343 | HARDENED, 0 | HARDENED, 0, 0],
            [44 | HARDENED, 343 | HARDENED, 9 | HARDENED, 0, 0],
            [44 | HARDENED, 343 | HARDENED, 9999 | HARDENED, 0, 0],
        ]

        for path in incorrect_paths:
            self.assertFalse(validate_full_path(path))

        for path in correct_paths:
            self.assertTrue(validate_full_path(path))


if __name__ == '__main__':
    unittest.main()
