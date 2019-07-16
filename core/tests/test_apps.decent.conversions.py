from common import *

from apps.decent import helpers

from trezor.messages.DecentObjectId import DecentObjectId

class TestDecentConversions(unittest.TestCase):
    def test_decent_object_id_to_string(self):
        object_ids_in = [
            DecentObjectId(id=72620543991349260),
            DecentObjectId(id=72620543991349265),
            DecentObjectId(id=147774362773094400),
            DecentObjectId(id=147774362773094403),
        ]
        object_ids_out = [
            '1.2.12',
            '1.2.17',
            '2.13.0',
            '2.13.3',
        ]
        for i, o in zip(object_ids_in, object_ids_out):
            self.assertEqual(helpers.object_id_to_string(i), o)

    def test_decent_vote_id_to_string(self):
        vote_id_in = [
            256,
            1792,
        ]
        vote_id_out = [
            '0:1',
            '0:7',
        ]
        for i, o in zip(vote_id_in, vote_id_out):
            self.assertEqual(helpers.vote_id_to_string(i), o)

if __name__ == '__main__':
    unittest.main()
