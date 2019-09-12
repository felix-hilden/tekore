import json
import unittest

from typing import List
from dataclasses import dataclass
from spotipy.serialise import SerialisableEnum, SerialisableDataclass, ModelList


class TestSerialisableEnum(unittest.TestCase):
    def test_enum_str_is_name(self):
        e = SerialisableEnum('e', 'a b c')
        self.assertEqual(str(e.a), 'a')


@dataclass
class Data(SerialisableDataclass):
    i: int


class TestSerialisableDataclass(unittest.TestCase):
    def test_dataclass_serialised(self):
        dict_in = {'i': 1}
        data = Data(**dict_in)
        dict_out = json.loads(str(data))
        self.assertDictEqual(dict_in, dict_out)

    def test_repr_intact(self):
        data = Data(i=1)
        self.assertTrue(repr(data).endswith('Data(i=1)'))

    def test_members_recursed_into(self):
        @dataclass
        class Container(SerialisableDataclass):
            d: List[Data]

            def __post_init__(self):
                self.d = [Data(**i) for i in self.d]

        dict_in = {'d': [{'i': 1}, {'i': 2}]}
        data = Container(**dict_in)
        dict_out = json.loads(str(data))
        self.assertDictEqual(dict_in, dict_out)


class TestModelList(unittest.TestCase):
    def test_list_of_dataclasses_serialised(self):
        list_in = [{'i': 1}, {'i': 2}]
        data = ModelList(Data(**i) for i in list_in)
        list_out = json.loads(str(data))
        self.assertListEqual(list_in, list_out)

    def test_repr_of_members_intact(self):
        list_in = [{'i': 1}, {'i': 2}]

        builtin = [Data(**i) for i in list_in]
        serialisable = ModelList(Data(**i) for i in list_in)

        self.assertEqual(repr(builtin), repr(serialisable))


if __name__ == '__main__':
    unittest.main()
