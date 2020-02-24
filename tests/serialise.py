import json
import unittest

from enum import Enum
from typing import List
from dataclasses import dataclass
from unittest.mock import MagicMock, patch

from tekore.serialise import (
    JSONEncoder,
    SerialisableDataclass,
    SerialisableEnum,
    ModelList,
    Timestamp,
)


class TestSerialisableEnum(unittest.TestCase):
    def test_enum_str_is_name(self):
        e = SerialisableEnum('e', 'a b c')
        self.assertEqual(str(e.a), 'a')


class TestJSONEncoder(unittest.TestCase):
    def test_enum_encoded_is_quoted_str(self):
        enum = Enum('enum', 'a b c')
        encoded = JSONEncoder().encode(enum.a)
        self.assertEqual(encoded, f'"{str(enum.a)}"')

    def test_default_types_preserved(self):
        d = {'items': 'in', 'this': 1}
        encoded = JSONEncoder().encode(d)
        default = json.dumps(d)
        self.assertEqual(encoded, default)

    def test_timestamp_encoded_is_quoted_str(self):
        t = Timestamp.from_string('2019-01-01T12:00:00Z')
        encoded = JSONEncoder().encode(t)

        self.assertEqual(encoded, f'"{str(t)}"')

    def test_non_serialisable_item_raises(self):
        class C:
            pass

        c = C()
        with self.assertRaises(TypeError):
            JSONEncoder().encode(c)


class TestTimestamp(unittest.TestCase):
    def test_timestamp_initialisable_from_string(self):
        Timestamp.from_string('2019-01-01T12:00:00Z')

    def test_incorrect_format_raises(self):
        with self.assertRaises(ValueError):
            Timestamp.from_string('2019-01-01')

    def test_timestamp_formatted_back_to_string(self):
        time_str = '2019-01-01T12:00:00Z'
        t = Timestamp.from_string(time_str)
        self.assertEqual(str(t), time_str)

    def test_initialisable_with_microsecond_precision(self):
        Timestamp.from_string('2019-01-01T12:00:00.000000Z')

    def test_initialisable_with_millisecond_precision(self):
        Timestamp.from_string('2019-01-01T12:00:00.00Z')


@dataclass(repr=False)
class Data(SerialisableDataclass):
    i: int


class TestSerialisableDataclass(unittest.TestCase):
    def test_dataclass_serialised(self):
        dict_in = {'i': 1}
        data = Data(**dict_in)
        dict_out = json.loads(str(data))
        self.assertDictEqual(dict_in, dict_out)

    def test_repr(self):
        data = Data(i=1)
        self.assertIn('Data', repr(data))

    def test_long_repr(self):
        @dataclass(repr=False)
        class LongContainer(SerialisableDataclass):
            attribute_1: int = 1
            attribute_2: int = 2
            attribute_3: int = 3
            attribute_4: int = 4
            attribute_5: int = 5

        @dataclass(repr=False)
        class LongData(SerialisableDataclass):
            data: LongContainer
            data_list: List[LongContainer]
            builtin_list: List[int]
            raw_dict: dict
            string: str
            boolean: bool

        data = LongData(
            LongContainer(),
            [LongContainer() for _ in range(20)],
            list(range(10)),
            {str(k): k for k in range(20)},
            'really long string which will most probably be cut off' * 2,
            True
        )
        repr(data)

    def test_asdict_members_recursed_into(self):
        @dataclass(repr=False)
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

        with patch('tekore.serialise.asdict', asdict):
            data.asdict()
            asdict.assert_called_with(data)

    def test_asdict_returns_dict_representation(self):
        data = Data(i=1)
        d = data.asdict()
        self.assertDictEqual(d, {'i': 1})

    def test_pprint_called_with_dict(self):
        pprint = MagicMock()
        data = Data(i=1)

        with patch('tekore.serialise.pprint', pprint):
            data.pprint()
            pprint.assert_called_with({'i': 1}, depth=None, compact=False)

    def test_keyword_arguments_passed_to_pprint(self):
        pprint = MagicMock()
        data = Data(i=1)
        kwargs = {
            'compact': False,
            'depth': None,
            'kw': 'argument'
        }

        with patch('tekore.serialise.pprint', pprint):
            data.pprint(**kwargs)
            pprint.assert_called_with({'i': 1}, **kwargs)

    def test_enum_in_dataclass(self):
        e = SerialisableEnum('e', 'a b c')

        @dataclass(repr=False)
        class C(SerialisableDataclass):
            v: e

        c = C(e.a)
        with self.subTest('No conversion in asdict'):
            self.assertIsInstance(c.asdict()['v'], SerialisableEnum)
        with self.subTest('Conversion in str'):
            self.assertEqual(str(c), '{"v": "a"}')

    def test_timestamp_in_dataclass(self):
        @dataclass(repr=False)
        class C(SerialisableDataclass):
            v: Timestamp

        c = C(Timestamp.from_string('2019-01-01T12:00:00Z'))
        with self.subTest('No conversion in asdict'):
            self.assertIsInstance(c.asdict()['v'], Timestamp)
        with self.subTest('Conversion in str'):
            self.assertEqual(str(c), '{"v": "2019-01-01T12:00:00Z"}')


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
