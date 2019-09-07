import unittest

from spotipy.enumerate import SerialisableEnum


class TestSerialisableEnum(unittest.TestCase):
    def test_enum_str_is_name(self):
        e = SerialisableEnum('e', 'a b c')
        self.assertEqual(str(e.a), 'a')


if __name__ == '__main__':
    unittest.main()
