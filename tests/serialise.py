import json
import unittest

from enum import Enum
from typing import List
from dataclasses import dataclass
from unittest.mock import MagicMock, patch

from spotipy.serialise import (
    JSONEncoder,
    SerialisableDataclass,
    SerialisableEnum,
    ModelList
)


class TestSerialisableEnum(unittest.TestCase):
    def test_enum_str_is_name(self):
        e = SerialisableEnum('e', 'a b c')
        self.assertEqual(str(e.a), 'a')


class TestJSONEncoder(unittest.TestCase):
    def test_enum_encoded_is_name(self):
        enum = Enum('enum', 'a b c')
        encoded = JSONEncoder().encode(enum.a)
        self.assertEqual(encoded, '"a"')

    def test_non_enum_encoded_is_preserved(self):
        d = {'items': 'in', 'this': 'dict'}
        encoded = JSONEncoder().encode(d)
        default = json.dumps(d)
        self.assertEqual(encoded, default)

    def test_non_serialisable_item_raises(self):
        class C:
            pass

        c = C()
        with self.assertRaises(TypeError):
            JSONEncoder().encode(c)


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

    def test_asdict_called_with_self(self):
        asdict = MagicMock(return_value='dict')
        data = Data(i=1)

        with patch('spotipy.serialise.asdict', asdict):
            data.asdict()
            asdict.assert_called_with(data)

    def test_asdict_returns_dict_representation(self):
        data = Data(i=1)
        d = data.asdict()
        self.assertDictEqual(d, {'i': 1})

    def test_pprint_called_with_dict(self):
        pprint = MagicMock()
        data = Data(i=1)

        with patch('spotipy.serialise.pprint', pprint):
            data.pprint()
            pprint.assert_called_with({'i': 1})

    def test_keyword_arguments_passed_to_pprint(self):
        pprint = MagicMock()
        data = Data(i=1)

        with patch('spotipy.serialise.pprint', pprint):
            data.pprint(kw='argument')
            pprint.assert_called_with({'i': 1}, kw='argument')


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
