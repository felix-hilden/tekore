import pytest

from tekore import Scope, scope


class TestScopesEnum:
    def test_str_is_enum_value(self):
        s = scope.user_read_private
        assert str(s) == "user-read-private"

    def test_subtracting_same_scope_returns_empty(self):
        s = scope.user_library_read - scope.user_library_read
        assert s == set()


class TestScope:
    def test_repr_like_instantiation(self):
        s = Scope("a", "b")
        assert repr(s) == "Scope('a', 'b')"

    def test_empty_scope_equal_to_empty_set(self):
        s = Scope()
        assert s == set()

    def test_scope_initialisable_with_strings(self):
        s = Scope("b", "a")
        assert str(s) == "a b"

    def test_scope_initialisable_with_enum(self):
        s = Scope(scope.user_read_private)
        assert str(s) == "user-read-private"

    def test_scope_initialisable_with_combination(self):
        s = Scope("a", "b", scope.user_read_private)
        assert str(s) == "a b user-read-private"

    def test_different_object_same_str_results_in_no_duplicates(self):
        s = Scope(scope.user_read_private, "user-read-private")
        assert s == {"user-read-private"}

    def test_scope_unpackable(self):
        s1 = Scope("b", "a")
        s2 = Scope(*s1)
        assert s1 == s2

    def test_adding_scopes_preserves_originals(self):
        s1 = Scope("b", "a")
        s2 = Scope("c", "b")

        assert isinstance(s1 + s2, Scope)
        assert s1 + s2 == {"a", "b", "c"}
        assert str(s1) == "a b"
        assert str(s2) == "b c"

    def test_subtracting_scopes_preservers_originals(self):
        s1 = Scope("b", "a")
        s2 = Scope("c", "b")

        assert isinstance(s1 - s2, Scope)
        assert s1 - s2 == {"a"}
        assert str(s1) == "a b"
        assert str(s2) == "b c"


class TestScopeOperations:
    def test_add_invalid_scope(self):
        with pytest.raises(NotImplementedError):
            1 + scope.user_top_read

    def test_add_invalid_scopeset(self):
        with pytest.raises(NotImplementedError):
            1 + Scope("a")

    def test_add_str_scope(self):
        s = "a" + scope.user_top_read
        assert str(s) == "a user-top-read"

    def test_add_str_scopeset(self):
        s = "a" + Scope("b")
        assert str(s) == "a b"

    def test_add_scope_str(self):
        s = scope.user_top_read + "a"
        assert str(s) == "a user-top-read"

    def test_add_scope_scope(self):
        s = scope.user_follow_read + scope.user_top_read
        assert str(s) == "user-follow-read user-top-read"

    def test_add_scope_scopeset(self):
        s = scope.user_top_read + Scope("a")
        assert str(s) == "a user-top-read"

    def test_add_scope_invalid_raises(self):
        with pytest.raises(NotImplementedError):
            scope.user_top_read + 1

    def test_add_scopeset_str(self):
        s = Scope("a") + "b"
        assert str(s) == "a b"

    def test_add_scopeset_scope(self):
        s = Scope("a") + scope.user_top_read
        assert str(s) == "a user-top-read"

    def test_add_scopeset_scopeset(self):
        s = Scope("a") + Scope("b")
        assert str(s) == "a b"

    def test_add_scopeset_invalid_raises(self):
        with pytest.raises(NotImplementedError):
            Scope("a") + 1

    def test_sub_invalid_scope(self):
        with pytest.raises(NotImplementedError):
            1 - scope.user_top_read

    def test_sub_invalid_scopeset(self):
        with pytest.raises(NotImplementedError):
            1 - Scope("a")

    def test_sub_str_scope_different(self):
        s = "a" - scope.user_top_read
        assert str(s) == "a"

    def test_sub_str_scope_same(self):
        s = "user-top-read" - scope.user_top_read
        assert str(s) == ""

    def test_sub_str_scopeset_different(self):
        s = "a" - Scope("b")
        assert str(s) == "a"

    def test_sub_str_scopeset_same(self):
        s = "a" - Scope("a")
        assert str(s) == ""

    def test_sub_scope_str_different(self):
        s = scope.user_top_read - "a"
        assert str(s) == "user-top-read"

    def test_sub_scope_str_same(self):
        s = scope.user_top_read - "user-top-read"
        assert str(s) == ""

    def test_sub_scope_scope_different(self):
        s = scope.user_top_read - scope.user_follow_read
        assert str(s) == "user-top-read"

    def test_sub_scope_scope_same(self):
        s = scope.user_top_read - scope.user_top_read
        assert str(s) == ""

    def test_sub_scope_scopeset_different(self):
        s = scope.user_top_read - Scope("a")
        assert str(s) == "user-top-read"

    def test_sub_scope_scopeset_same(self):
        s = scope.user_top_read - Scope("user-top-read")
        assert str(s) == ""

    def test_sub_scope_invalid_raises(self):
        with pytest.raises(NotImplementedError):
            scope.user_top_read - 1

    def test_sub_scopeset_str_different(self):
        s = Scope("a") - "b"
        assert str(s) == "a"

    def test_sub_scopeset_str_same(self):
        s = Scope("a") - "a"
        assert str(s) == ""

    def test_sub_scopeset_scope_different(self):
        s = Scope("a") - scope.user_top_read
        assert str(s) == "a"

    def test_sub_scopeset_scope_same(self):
        s = Scope("user-top-read") - scope.user_top_read
        assert str(s) == ""

    def test_sub_scopeset_scopeset_different(self):
        s = Scope("a") - Scope("b")
        assert str(s) == "a"

    def test_sub_scopeset_scopeset_same(self):
        s = Scope("a") - Scope("a")
        assert str(s) == ""

    def test_sub_scopeset_invalid_raises(self):
        with pytest.raises(NotImplementedError):
            Scope("a") - 1
