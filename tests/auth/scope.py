import pytest
from tekore import scope, Scope


class TestScopesEnum:
    def test_str_is_enum_value(self):
        """
        Return true if the value is a string.

        Args:
            self: (todo): write your description
        """
        s = scope.user_read_private
        assert str(s) == 'user-read-private'

    def test_subtracting_same_scope_returns_empty(self):
        """
        Return true if the given set of test test test sets of test test variables.

        Args:
            self: (todo): write your description
        """
        s = scope.user_library_read - scope.user_library_read
        assert s == set()


class TestScope:
    def test_repr_like_instantiation(self):
        """
        Print a repr_repr_repr ()

        Args:
            self: (todo): write your description
        """
        s = Scope('a', 'b')
        assert repr(s) == "Scope('a', 'b')"

    def test_empty_scope_equal_to_empty_set(self):
        """
        Returns a set of empty.

        Args:
            self: (todo): write your description
        """
        s = Scope()
        assert s == set()

    def test_scope_initialisable_with_strings(self):
        """
        Sets initial scope scope.

        Args:
            self: (todo): write your description
        """
        s = Scope('b', 'a')
        assert str(s) == 'a b'

    def test_scope_initialisable_with_enum(self):
        """
        : return : py : func : ~tax.

        Args:
            self: (todo): write your description
        """
        s = Scope(scope.user_read_private)
        assert str(s) == 'user-read-private'

    def test_scope_initialisable_with_combination(self):
        """
        Returns the initial scope scope.

        Args:
            self: (todo): write your description
        """
        s = Scope('a', 'b', scope.user_read_private)
        assert str(s) == 'a b user-read-private'

    def test_different_object_same_str_results_in_no_duplicates(self):
        """
        Returns true if the user - allowed test set.

        Args:
            self: (todo): write your description
        """
        s = Scope(scope.user_read_private, 'user-read-private')
        assert s == {'user-read-private'}

    def test_scope_unpackable(self):
        """
        Unpack the scope of the scope.

        Args:
            self: (todo): write your description
        """
        s1 = Scope('b', 'a')
        s2 = Scope(*s1)
        assert s1 == s2

    def test_adding_scopes_preserves_originals(self):
        """
        Test for the test test to be used by default.

        Args:
            self: (todo): write your description
        """
        s1 = Scope('b', 'a')
        s2 = Scope('c', 'b')

        assert isinstance(s1 + s2, Scope)
        assert s1 + s2 == {'a', 'b', 'c'}
        assert str(s1) == 'a b'
        assert str(s2) == 'b c'

    def test_subtracting_scopes_preservers_originals(self):
        """
        Test if the presence of scopes are allowed.

        Args:
            self: (todo): write your description
        """
        s1 = Scope('b', 'a')
        s2 = Scope('c', 'b')

        assert isinstance(s1 - s2, Scope)
        assert s1 - s2 == {'a'}
        assert str(s1) == 'a b'
        assert str(s2) == 'b c'


class TestScopeOperations:
    def test_add_invalid_scope(self):
        """
        Add the test scope to the scope.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(NotImplementedError):
            1 + scope.user_top_read

    def test_add_invalid_Scope(self):
        """
        A test test test to test.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(NotImplementedError):
            1 + Scope('a')

    def test_add_str_scope(self):
        """
        Add the test scope to the scope.

        Args:
            self: (todo): write your description
        """
        s = 'a' + scope.user_top_read
        assert str(s) == 'a user-top-read'

    def test_add_str_Scope(self):
        """
        Add a string to string.

        Args:
            self: (todo): write your description
        """
        s = 'a' + Scope('b')
        assert str(s) == 'a b'

    def test_add_scope_str(self):
        """
        Add the test scope scope scope.

        Args:
            self: (todo): write your description
        """
        s = scope.user_top_read + 'a'
        assert str(s) == 'a user-top-read'

    def test_add_scope_scope(self):
        """
        Add the test scope scope to the scope.

        Args:
            self: (todo): write your description
        """
        s = scope.user_follow_read + scope.user_top_read
        assert str(s) == 'user-follow-read user-top-read'

    def test_add_scope_Scope(self):
        """
        Set the test scope scope to the scope.

        Args:
            self: (todo): write your description
        """
        s = scope.user_top_read + Scope('a')
        assert str(s) == 'a user-top-read'

    def test_add_scope_invalid_raises(self):
        """
        Add the test test test test for the test.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(NotImplementedError):
            scope.user_top_read + 1

    def test_add_Scope_str(self):
        """
        Add a string to string.

        Args:
            self: (todo): write your description
        """
        s = Scope('a') + 'b'
        assert str(s) == 'a b'

    def test_add_Scope_scope(self):
        """
        Set the test scope to the scope.

        Args:
            self: (todo): write your description
        """
        s = Scope('a') + scope.user_top_read
        assert str(s) == 'a user-top-read'

    def test_add_Scope_Scope(self):
        """
        Add test test test string.

        Args:
            self: (todo): write your description
        """
        s = Scope('a') + Scope('b')
        assert str(s) == 'a b'

    def test_add_Scope_invalid_raises(self):
        """
        Add test test test to test.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(NotImplementedError):
            Scope('a') + 1

    def test_sub_invalid_scope(self):
        """
        : return : py : return :

        Args:
            self: (todo): write your description
        """
        with pytest.raises(NotImplementedError):
            1 - scope.user_top_read

    def test_sub_invalid_Scope(self):
        """
        Validate that the test is in the test.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(NotImplementedError):
            1 - Scope('a')

    def test_sub_str_scope_different(self):
        """
        Test if the current scope is allowed.

        Args:
            self: (todo): write your description
        """
        s = 'a' - scope.user_top_read
        assert str(s) == 'a'

    def test_sub_str_scope_same(self):
        """
        Returns true if the current scope.

        Args:
            self: (todo): write your description
        """
        s = 'user-top-read' - scope.user_top_read
        assert str(s) == ''

    def test_sub_str_Scope_different(self):
        """
        R sub - ]

        Args:
            self: (todo): write your description
        """
        s = 'a' - Scope('b')
        assert str(s) == 'a'

    def test_sub_str_Scope_same(self):
        """
        Test if sub sub sub sub sub sub - test test test.

        Args:
            self: (todo): write your description
        """
        s = 'a' - Scope('a')
        assert str(s) == ''

    def test_sub_scope_str_different(self):
        """
        Test if the current scope is allowed scope.

        Args:
            self: (todo): write your description
        """
        s = scope.user_top_read - 'a'
        assert str(s) == 'user-top-read'

    def test_sub_scope_str_same(self):
        """
        Test if the sub - sub - test sub - scope.

        Args:
            self: (todo): write your description
        """
        s = scope.user_top_read - 'user-top-read'
        assert str(s) == ''

    def test_sub_scope_scope_different(self):
        """
        Test if the current scope is in.

        Args:
            self: (todo): write your description
        """
        s = scope.user_top_read - scope.user_follow_read
        assert str(s) == 'user-top-read'

    def test_sub_scope_scope_same(self):
        """
        Test if the current scope of the sub - scope.

        Args:
            self: (todo): write your description
        """
        s = scope.user_top_read - scope.user_top_read
        assert str(s) == ''

    def test_sub_scope_Scope_different(self):
        """
        Test if the current scope is allowed.

        Args:
            self: (todo): write your description
        """
        s = scope.user_top_read - Scope('a')
        assert str(s) == 'user-top-read'

    def test_sub_scope_Scope_same(self):
        """
        Returns true if the sub - sub sub - test.

        Args:
            self: (todo): write your description
        """
        s = scope.user_top_read - Scope('user-top-read')
        assert str(s) == ''

    def test_sub_scope_invalid_raises(self):
        """
        Test if the test scope is valid.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(NotImplementedError):
            scope.user_top_read - 1

    def test_sub_Scope_str_different(self):
        """
        R sub sub - string ]

        Args:
            self: (todo): write your description
        """
        s = Scope('a') - 'b'
        assert str(s) == 'a'

    def test_sub_Scope_str_same(self):
        """
        Check if the sub sub sub sub sub sub - string of - fields_same as sub_sub - test.

        Args:
            self: (todo): write your description
        """
        s = Scope('a') - 'a'
        assert str(s) == ''

    def test_sub_Scope_scope_different(self):
        """
        Test if the scope is allowed.

        Args:
            self: (todo): write your description
        """
        s = Scope('a') - scope.user_top_read
        assert str(s) == 'a'

    def test_sub_Scope_scope_same(self):
        """
        Returns true if the scope is in the same scope.

        Args:
            self: (todo): write your description
        """
        s = Scope('user-top-read') - scope.user_top_read
        assert str(s) == ''

    def test_sub_Scope_Scope_different(self):
        """
        R \ ~ ] is a valid test.

        Args:
            self: (todo): write your description
        """
        s = Scope('a') - Scope('b')
        assert str(s) == 'a'

    def test_sub_Scope_Scope_same(self):
        """
        R test test test test test test sub test.

        Args:
            self: (todo): write your description
        """
        s = Scope('a') - Scope('a')
        assert str(s) == ''

    def test_sub_Scope_invalid_raises(self):
        """
        Validate that the test test test is valid.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(NotImplementedError):
            Scope('a') - 1
