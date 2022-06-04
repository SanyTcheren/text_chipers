"""Test for coder/decoder."""

import unittest
from coder_decoder import Coder, Decoder
import code_exc as exc


class TestCoder(unittest.TestCase):
    """Test coder."""

    def setUp(self):
        self.table = {
            'village': 'enemy',
            'roanoke': 'cavalry',
            'goodwin': 'tennessee',
            'snow': 'rebels'
        }
        self.text = 'Enemy cavalry heading to Tennessee with Rebels gone ' +\
            'you are free to transport your supplies south'
        self.code = 'rest transport you goodwin village ' +\
            'roanoke with are your is just supplies free ' +\
            'snow heading to gone to south filler'
        self.coder = Coder([-1, 2, -3, 4], self.table)

    def test_add_table(self):
        """Test add_table."""
        table = {
            'star': 'water'
        }
        self.coder.add_table(table)
        self.assertEqual(self.coder.table, self.table | table)

    def test_encode(self):
        """Test encode."""
        self.assertEqual(self.coder.encode(self.text, 20), self.code)
        self.assertRaises(exc.LengthSmall, self.coder.encode, self.text, 12)
        self.assertRaises(exc.LengthNotKey, self.coder.encode, self.text, 19)


class TestDecoder(unittest.TestCase):
    """Test decoder."""

    def setUp(self):
        self.table = {
            'village': 'enemy',
            'roanoke': 'cavalry',
            'goodwin': 'tennessee',
            'snow': 'rebels'
        }
        self.text = 'enemy cavalry heading to tennessee with rebels gone ' +\
            'you are free to transport your supplies south'
        self.code = 'rest transport you goodwin village ' +\
            'roanoke with are your is just supplies free ' +\
            'snow heading to gone to south filler'
        self.decoder = Decoder([-1, 2, -3, 4], self.table)

    def test_decode(self):
        """Test decoder."""
        self.assertEqual(self.decoder.decode(self.code, 16), self.text)

    def test_check(self):
        """Test check_key."""
        self.assertTrue(self.decoder.check_key(self.code))
        test_code = ' '.join(self.code.split()[:-2])
        self.assertRaises(
            exc.KeyNotLength,
            self.decoder.check_key, test_code)


if __name__ == '__main__':
    unittest.main()
