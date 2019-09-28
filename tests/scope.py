import unittest

from spotipy.scope import AuthorisationScopes, Scope


class TestAuthorisationScopes(unittest.TestCase):
    def test_str_is_enum_value(self):
        s = AuthorisationScopes.user_read_private
        self.assertEqual(str(s), 'user-read-private')


class TestScope(unittest.TestCase):
    def test_empty_scope_initialisable(self):
        Scope()

    def test_scope_initialisable_with_strings(self):
        s = Scope('b', 'a')
        self.assertEqual(str(s), 'a b')

    def test_scope_initialisable_with_enum(self):
        s = Scope(AuthorisationScopes.user_read_private)
        self.assertEqual(str(s), 'user-read-private')

    def test_scope_initialisable_with_combination(self):
        s = Scope(
            'a',
            'b',
            AuthorisationScopes.user_read_private
        )
        self.assertEqual(str(s), 'a b user-read-private')

    def test_scope_initialisable_with_another_scope(self):
        s1 = Scope('b', 'a')
        s2 = Scope(s1)
        self.assertSetEqual(s1, s2)

    def test_different_object_same_str_results_in_no_duplicates(self):
        s = Scope(AuthorisationScopes.user_read_private, 'user-read-private')
        self.assertSetEqual(s, {'user-read-private'})

    def test_scope_unpackable(self):
        s1 = Scope('b', 'a')
        s2 = Scope(*s1)
        self.assertSetEqual(s1, s2)

    def test_adding_scopes_returns_scope(self):
        s1 = Scope('b', 'a')
        s2 = Scope('c', 'b')
        self.assertIsInstance(s1 + s2, Scope)

    def test_adding_scopes_returns_union(self):
        s1 = Scope('b', 'a')
        s2 = Scope('c', 'b')
        self.assertSetEqual(s1 + s2, {'a', 'b', 'c'})

    def test_adding_set_returns_union(self):
        s1 = Scope('b', 'a')
        s2 = {'c', 'b'}
        self.assertSetEqual(s1 + s2, {'a', 'b', 'c'})

    def test_adding_str_converts_to_set(self):
        s1 = Scope('b', 'a')
        s2 = 'c'
        self.assertSetEqual(s1 + s2, {'a', 'b', 'c'})

    def test_adding_authorisation_scope_converts_to_set(self):
        s1 = Scope('a')
        s2 = AuthorisationScopes.user_read_private
        self.assertSetEqual(s1 + s2, {'user-read-private', 'a'})

    def test_subtracting_scopes_returns_scope(self):
        s1 = Scope('b', 'a')
        s2 = Scope('c', 'b')
        self.assertIsInstance(s1 - s2, Scope)

    def test_subtracting_scopes_returns_relative_complement(self):
        s1 = Scope('b', 'a')
        s2 = Scope('c', 'b')
        self.assertSetEqual(s1 - s2, {'a'})

    def test_subtracting_set_returns_relative_complement(self):
        s1 = Scope('b', 'a')
        s2 = {'c', 'b'}
        self.assertSetEqual(s1 - s2, {'a'})

    def test_subtracting_str_converts_to_set(self):
        s1 = Scope('b', 'a')
        s2 = 'b'
        self.assertSetEqual(s1 - s2, {'a'})

    def test_subtracting_authorisation_scope_converts_to_set(self):
        s1 = Scope('user-read-private', 'a')
        s2 = AuthorisationScopes.user_read_private
        self.assertSetEqual(s1 - s2, {'a'})
