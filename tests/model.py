from datetime import datetime

import pytest

from tekore._model.serialise import Model, StrEnum, UnknownModelAttributeWarning


class E(StrEnum):
    a = "a"
    b = "b"
    c = "c"


class ECaps(StrEnum):
    a = "A"
    b = "B"
    c = "C"


class TestEnumCaseInsensitive:
    def test_all_caps(self):
        assert E["A"] == E.a
        assert E["B"] == E.b
        assert E["C"] == E.c

    def test_all_lowercase(self):
        assert E["a"] is E.a
        assert E["b"] is E.b
        assert E["c"] is E.c

    def test_in_caps(self):
        assert ECaps.a in ECaps
        assert ECaps.b in ECaps
        assert ECaps.c in ECaps

    def test_all_caps_caps_keys(self):
        assert ECaps["A"] == ECaps.a
        assert ECaps["B"] == ECaps.b
        assert ECaps["C"] == ECaps.c

    def test_all_lowercase_caps_keys(self):
        assert ECaps["a"] is ECaps.a
        assert ECaps["b"] is ECaps.b
        assert ECaps["c"] is ECaps.c

    def test_non_destructive_iter(self):
        # Should not change caps when iterating or accessing values in other means
        for e in ECaps:
            assert e.upper() == e


class TestSerialisableEnum:
    def test_enum_repr_shows_enum(self):
        assert "E.a" in repr(E.a)

    def test_enum_str_is_name(self):
        e = StrEnum("e", "a b c")
        assert str(e.a) == "a"

    def test_enum_is_sortable(self):
        enums = list(E)[::-1]
        assert sorted(enums) == enums[::-1]


class TestModel:
    def test_enum_in_model(self):
        class C(Model):
            v: E

        c = C(v=E.a)
        assert isinstance(c.model_dump()["v"], str)
        assert c.model_dump_json() == '{"v":"a"}'

    def test_timestamps_in_model(self):
        class C(Model):
            v: datetime

        C(v="2019-01-01T12:00:00Z")
        C(v="2019-01-01T12:00:00.1234Z")

    def test_unknown_attribute_ignored(self):
        class Data(Model):
            i: int

        with pytest.warns(UnknownModelAttributeWarning):
            data = Data(i=1, u=2)

        with pytest.raises(AttributeError):
            assert data.u
        assert "u" not in data.model_dump_json()
