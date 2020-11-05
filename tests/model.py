import json
import pytest

from enum import Enum
from typing import List
from dataclasses import dataclass
from unittest.mock import MagicMock, patch

from tekore._model.serialise import (
    JSONEncoder,
    Model,
    StrEnum,
    ModelList,
    Timestamp,
)


class E(StrEnum):
    a = 'a'
    b = 'b'
    c = 'c'


class TestSerialisableEnum:
    def test_enum_repr_shows_enum(self):
        """
        Return the enum enum enum type.

        Args:
            self: (todo): write your description
        """
        assert 'E.a' in repr(E.a)

    def test_enum_str_is_name(self):
        """
        Returns true if the string is a string.

        Args:
            self: (todo): write your description
        """
        e = StrEnum('e', 'a b c')
        assert str(e.a) == 'a'

    def test_enum_is_sortable(self):
        """
        Return a list of enum enum enum names.

        Args:
            self: (todo): write your description
        """
        enums = list(E)[::-1]
        assert sorted(enums) == enums[::-1]


class TestJSONEncoder:
    def test_enum_encoded_is_quoted_str(self):
        """
        : return : attr : encoded_enum_encoded_str_encoded.

        Args:
            self: (todo): write your description
        """
        enum = Enum('enum', 'a b c')
        encoded = JSONEncoder().encode(enum.a)
        assert encoded == f'"{str(enum.a)}"'

    def test_default_types_preserved(self):
        """
        : return : attr : ~

        Args:
            self: (todo): write your description
        """
        d = {'items': 'in', 'this': 1}
        encoded = JSONEncoder().encode(d)
        default = json.dumps(d)
        assert encoded == default

    def test_timestamp_encoded_is_quoted_str(self):
        """
        : return :

        Args:
            self: (todo): write your description
        """
        t = Timestamp.from_string('2019-01-01T12:00:00Z')
        encoded = JSONEncoder().encode(t)

        assert encoded == f'"{str(t)}"'

    def test_non_serialisable_item_raises(self):
        """
        Sets the serialized item item as json.

        Args:
            self: (todo): write your description
        """
        class C:
            pass

        c = C()
        with pytest.raises(TypeError):
            JSONEncoder().encode(c)


class TestTimestamp:
    def test_timestamp_initialisable_from_string(self):
        """
        Test if the timestamp : py : return : return :

        Args:
            self: (todo): write your description
        """
        Timestamp.from_string('2019-01-01T12:00:00Z')

    def test_incorrect_format_raises(self):
        """
        Set the test test test string.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(ValueError):
            Timestamp.from_string('2019-01-01')

    def test_timestamp_formatted_back_to_string(self):
        """
        Test if a timestamp was modified.

        Args:
            self: (todo): write your description
        """
        time_str = '2019-01-01T12:00:00Z'
        t = Timestamp.from_string(time_str)
        assert str(t) == time_str

    def test_initialisable_with_microsecond_precision(self):
        """
        Test for micro microsecond test.

        Args:
            self: (todo): write your description
        """
        Timestamp.from_string('2019-01-01T12:00:00.000000Z')

    def test_initialisable_with_millisecond_precision(self):
        """
        Set the initial test test for the test

        Args:
            self: (todo): write your description
        """
        Timestamp.from_string('2019-01-01T12:00:00.00Z')


@dataclass(repr=False)
class Data(Model):
    i: int


module = 'tekore._model.serialise'


class TestSerialisableDataclass:
    def test_json_dataclass_serialised(self):
        """
        Test if serialised dataclass json serialised.

        Args:
            self: (todo): write your description
        """
        dict_in = {'i': 1}
        data = Data(**dict_in)
        dict_out = json.loads(data.json())
        assert dict_in == dict_out

    def test_repr(self):
        """
        Print the test data

        Args:
            self: (todo): write your description
        """
        data = Data(i=1)
        assert 'Data' in repr(data)

    def test_long_repr(self):
        """
        Test if a list of integers.

        Args:
            self: (todo): write your description
        """
        @dataclass(repr=False)
        class LongContainer(Model):
            attribute_1: int = 1
            attribute_2: int = 2
            attribute_3: int = 3
            attribute_4: int = 4
            attribute_5: int = 5

        @dataclass(repr=False)
        class LongData(Model):
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

    def test_asbuiltin_members_recursed_into(self):
        """
        Test if members of the members arebuilt. *

        Args:
            self: (todo): write your description
        """
        @dataclass(repr=False)
        class Container(Model):
            d: List[Data]

            def __post_init__(self):
                """
                Do some setup after initialisation.

                Args:
                    self: (todo): write your description
                """
                self.d = [Data(**i) for i in self.d]

        dict_in = {'d': [{'i': 1}, {'i': 2}]}
        data = Container(**dict_in)
        dict_out = data.asbuiltin()
        assert dict_in == dict_out

    def test_asbuiltin_returns_dict_representation(self):
        """
        Return a dict of dicts in the keys.

        Args:
            self: (todo): write your description
        """
        data = Data(i=1)
        d = data.asbuiltin()
        assert d == {'i': 1}

    def test_pprint_called_with_dict(self):
        """
        Test if the test data

        Args:
            self: (todo): write your description
        """
        pprint = MagicMock()
        data = Data(i=1)

        with patch(module + '.pprint', pprint):
            data.pprint()
            pprint.assert_called_with({'i': 1}, depth=None, compact=True)

    def test_keyword_arguments_passed_to_pprint(self):
        """
        Test if keyword arguments.

        Args:
            self: (todo): write your description
        """
        pprint = MagicMock()
        data = Data(i=1)
        kwargs = {
            'compact': False,
            'depth': None,
            'kw': 'argument'
        }

        with patch(module + '.pprint', pprint):
            data.pprint(**kwargs)
            pprint.assert_called_with({'i': 1}, **kwargs)

    def test_enum_in_dataclass(self):
        """
        Test if the given class exists in the given class.

        Args:
            self: (todo): write your description
        """
        @dataclass(repr=False)
        class C(Model):
            v: E

        c = C(E.a)
        assert isinstance(c.asbuiltin()['v'], str)
        assert c.json() == '{"v": "a"}'

    def test_timestamp_in_dataclass(self):
        """
        Test if a timestamp exists in the timestamp.

        Args:
            self: (todo): write your description
        """
        @dataclass(repr=False)
        class C(Model):
            v: Timestamp

        c = C(Timestamp.from_string('2019-01-01T12:00:00Z'))
        assert isinstance(c.asbuiltin()['v'], str)
        assert c.json() == '{"v": "2019-01-01T12:00:00Z"}'


class TestModelList:
    def test_list_of_dataclasses_serialised(self):
        """
        Returns a list of dataclasses.

        Args:
            self: (todo): write your description
        """
        list_in = [{'i': 1}, {'i': 2}]
        data = ModelList(Data(**i) for i in list_in)
        list_out = json.loads(data.json())
        assert list_in == list_out

    def test_repr(self):
        """
        Return a list of test test test data.

        Args:
            self: (todo): write your description
        """
        list_in = [{'i': 1}, {'i': 2}]
        data = ModelList(Data(**i) for i in list_in)

        assert 'Data' in repr(data)
