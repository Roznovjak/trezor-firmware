# This file is part of the Trezor project.
#
# Copyright (C) 2012-2018 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import time

import pytest

from trezorlib import decent
from trezorlib.messages import DecentSignedTx
from trezorlib.tools import parse_path

from .common import TrezorTest

CHAIN_ID = "02cdaed71517c2251f87d7c838a2bad0d193bddcfc53eae8ea788fb0e059d434"
ADDRESS_N = parse_path("m/44'/343'/0'/0/0")


@pytest.mark.skip_t1
@pytest.mark.decent
class TestMsgDecentSignTx(TrezorTest):
    def input_flow(self, pages):
        # confirm number of actions
        yield
        self.client.debug.press_yes()

        # swipe through pages
        yield
        for _ in range(pages - 1):
            self.client.debug.swipe_down()
            time.sleep(1)

        # confirm last page
        self.client.debug.press_yes()

    def test_decent_signtx_transfer_token(self):
        self.setup_mnemonic_nopin_nopassphrase()
        transaction = {
            "ref_block_num": 33226,
            "ref_block_prefix": 2134188895,
            "expiration": "2019-07-11T12:16:25",
            "operations": [
                [
                    39,
                    {
                        "fee": {"amount": 100000, "asset_id": "1.3.0"},
                        "from": "1.2.38",
                        "to": "1.2.39",
                        "amount": {"amount": 100000000, "asset_id": "1.3.0"},
                        "memo": {
                            "from": "DCT7qd59RnZtJC7d6cFvXYnFmdjtBJkg2DxizoSYVcJgexvUk9GFA",
                            "to": "DCT6kiy7aHbjNwxeFmkVN8r1KyCgNxaAXYr9uaEPHmvwuZNuhnodJ",
                            "nonce": "16718924664158993304",
                            "message": "eddb46c6feecdad252eaef73be98e8e0",
                        },
                        "extensions": [],
                    },
                ]
            ],
            "extensions": [],
        }

        with self.client:
            self.client.set_input_flow(self.input_flow(pages=4))
            resp = decent.sign_tx(self.client, ADDRESS_N, transaction, CHAIN_ID)
            assert isinstance(resp, DecentSignedTx)
            assert (
                resp.signature
                == "1f2ebd6f6310516883519b2aa0c44fd51f2b59a3b4c6babd5e44014ec6b353be6a09c592f83c323fd0df6511368a31a969a77ee31dae805c560f84a339b7719557"
            )

    def test_decent_signtx_account_create(self):
        self.setup_mnemonic_nopin_nopassphrase()
        transaction = {
            "ref_block_num": 33075,
            "ref_block_prefix": 215006047,
            "expiration": "2019-07-11T12:03:50",
            "operations": [
                [
                    1,
                    {
                        "fee": {"amount": 100000, "asset_id": "1.3.0"},
                        "registrar": "1.2.38",
                        "name": "new-account",
                        "owner": {
                            "weight_threshold": 1,
                            "account_auths": [],
                            "key_auths": [
                                [
                                    "DCT6kiy7aHbjNwxeFmkVN8r1KyCgNxaAXYr9uaEPHmvwuZNuhnodJ",
                                    1,
                                ]
                            ],
                        },
                        "active": {
                            "weight_threshold": 1,
                            "account_auths": [],
                            "key_auths": [
                                [
                                    "DCT6kiy7aHbjNwxeFmkVN8r1KyCgNxaAXYr9uaEPHmvwuZNuhnodJ",
                                    1,
                                ]
                            ],
                        },
                        "options": {
                            "memo_key": "DCT6kiy7aHbjNwxeFmkVN8r1KyCgNxaAXYr9uaEPHmvwuZNuhnodJ",
                            "voting_account": "1.2.3",
                            "num_miner": 0,
                            "votes": [],
                            "extensions": [],
                            "allow_subscription": False,
                            "price_per_subscribe": {"amount": 0, "asset_id": "1.3.0"},
                            "subscription_period": 0,
                        },
                        "extensions": {},
                    },
                ]
            ],
            "extensions": [],
        }

        with self.client:
            self.client.set_input_flow(self.input_flow(pages=11))
            resp = decent.sign_tx(self.client, ADDRESS_N, transaction, CHAIN_ID)
            assert isinstance(resp, DecentSignedTx)
            assert (
                resp.signature
                == "1f13d39426bfbffceee802d40e64da633cd09ccf89ba8d8a92ed5e5f519ffb4181123f197a4f36655ffb8a2e7f04d96b42c778f9098ec570e93ab05f079ec30c42"
            )

    def test_decent_signtx_account_update(self):
        self.setup_mnemonic_nopin_nopassphrase()
        transaction = {
            "ref_block_num": 33399,
            "ref_block_prefix": 2159546263,
            "expiration": "2019-07-11T12:30:50",
            "operations": [
                [
                    2,
                    {
                        "fee": {"amount": 100000, "asset_id": "1.3.0"},
                        "account": "1.2.38",
                        "active": {
                            "weight_threshold": 1,
                            "account_auths": [],
                            "key_auths": [
                                [
                                    "DCT6kiy7aHbjNwxeFmkVN8r1KyCgNxaAXYr9uaEPHmvwuZNuhnodJ",
                                    1,
                                ]
                            ],
                        },
                        "new_options": {
                            "memo_key": "DCT6kiy7aHbjNwxeFmkVN8r1KyCgNxaAXYr9uaEPHmvwuZNuhnodJ",
                            "voting_account": "1.2.39",
                            "num_miner": 1,
                            "votes": ["0:7"],
                            "extensions": [],
                            "allow_subscription": True,
                            "price_per_subscribe": {
                                "amount": 10000,
                                "asset_id": "1.3.1",
                            },
                            "subscription_period": 1,
                        },
                        "extensions": {},
                    },
                ]
            ],
            "extensions": [],
        }

        with self.client:
            self.client.set_input_flow(self.input_flow(pages=8))
            resp = decent.sign_tx(self.client, ADDRESS_N, transaction, CHAIN_ID)
            assert isinstance(resp, DecentSignedTx)
            assert (
                resp.signature
                == "207e4c77a657f9fae53a501ea89f6a1f0ec792ba18b3be7fafa92431b4fbdea7bd3f1ccc731d74ad53c217fbb66ab977ad666b8fe1ecb229106d662fd6617a3658"
            )

    def test_eos_signtx_multiple_operations(self):
        self.setup_mnemonic_nopin_nopassphrase()
        transaction = {
            "ref_block_num": 47496,
            "ref_block_prefix": 235616862,
            "expiration": "2019-07-12T08:05:50",
            "operations": [
                [
                    39,
                    {
                        "fee": {"amount": 100000, "asset_id": "1.3.0"},
                        "from": "1.2.38",
                        "to": "1.2.15",
                        "amount": {"amount": "10000000000", "asset_id": "1.3.0"},
                        "extensions": [],
                    },
                ],
                [
                    1,
                    {
                        "fee": {"amount": 100000, "asset_id": "1.3.0"},
                        "registrar": "1.2.38",
                        "name": "new-account",
                        "owner": {
                            "weight_threshold": 2,
                            "account_auths": [["1.2.15", 1], ["1.2.38", 2]],
                            "key_auths": [
                                [
                                    "DCT6kiy7aHbjNwxeFmkVN8r1KyCgNxaAXYr9uaEPHmvwuZNuhnodJ",
                                    1,
                                ]
                            ],
                        },
                        "active": {
                            "weight_threshold": 1,
                            "account_auths": [],
                            "key_auths": [
                                [
                                    "DCT6kiy7aHbjNwxeFmkVN8r1KyCgNxaAXYr9uaEPHmvwuZNuhnodJ",
                                    1,
                                ],
                                [
                                    "DCT7qd59RnZtJC7d6cFvXYnFmdjtBJkg2DxizoSYVcJgexvUk9GFA",
                                    1,
                                ],
                            ],
                        },
                        "options": {
                            "memo_key": "DCT6kiy7aHbjNwxeFmkVN8r1KyCgNxaAXYr9uaEPHmvwuZNuhnodJ",
                            "voting_account": "1.2.3",
                            "num_miner": 5,
                            "votes": ["0:1", "0:2", "0:3", "0:4", "0:5"],
                            "extensions": [],
                            "allow_subscription": True,
                            "price_per_subscribe": {
                                "amount": "100000000000",
                                "asset_id": "1.3.0",
                            },
                            "subscription_period": 7,
                        },
                        "extensions": {},
                    },
                ],
                [
                    2,
                    {
                        "fee": {"amount": 100000, "asset_id": "1.3.0"},
                        "account": "1.2.38",
                        "active": {
                            "weight_threshold": 1,
                            "account_auths": [],
                            "key_auths": [
                                [
                                    "DCT6kiy7aHbjNwxeFmkVN8r1KyCgNxaAXYr9uaEPHmvwuZNuhnodJ",
                                    1,
                                ]
                            ],
                        },
                        "new_options": {
                            "memo_key": "DCT6kiy7aHbjNwxeFmkVN8r1KyCgNxaAXYr9uaEPHmvwuZNuhnodJ",
                            "voting_account": "1.2.15",
                            "num_miner": 0,
                            "votes": [],
                            "extensions": [],
                            "allow_subscription": False,
                            "price_per_subscribe": {
                                "amount": 10000,
                                "asset_id": "1.3.1",
                            },
                            "subscription_period": 5,
                        },
                        "extensions": {},
                    },
                ],
            ],
            "extensions": [],
        }

        def input_flow():
            # confirm number of actions
            yield
            self.client.debug.press_yes()

            # swipe through transfer
            yield
            for _ in range(3):
                self.client.debug.swipe_down()
                time.sleep(1)

            # confirm transfer
            self.client.debug.press_yes()

            # swipe through create account
            yield
            for _ in range(15):
                self.client.debug.swipe_down()
                time.sleep(1)

            # confirm create account
            self.client.debug.press_yes()

            # swipe through update account
            yield
            for _ in range(7):
                self.client.debug.swipe_down()
                time.sleep(1)

            # confirm update account
            self.client.debug.press_yes()

        with self.client:
            self.client.set_input_flow(input_flow)
            resp = decent.sign_tx(self.client, ADDRESS_N, transaction, CHAIN_ID)
            assert isinstance(resp, DecentSignedTx)
            assert (
                resp.signature
                == "1f5a3fad5e9856d359ad436f9507630cf36b079d93813b77fe4c10516aaaf66e205c876068c5caa47c553a9723f36c40e072254da518afbe61a08e34debc0d6026"
            )
