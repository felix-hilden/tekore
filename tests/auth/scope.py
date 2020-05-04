import unittest
from tekore import scope, Scope


class TestAuthorisationScopes(unittest.TestCase):
    def test_str_is_enum_value(self):
        s = scope.user_read_private
        self.assertEqual(str(s), 'user-read-private')

    def test_addition(self):
        s = scope.user_library_read + scope.user_read_private

        with self.subTest('Returns scope'):
            self.assertIsInstance(s, Scope)

        with self.subTest('Returns correct members'):
            self.assertEqual(str(s), 'user-library-read user-read-private')

    def test_subtraction(self):
        s = scope.user_read_private - scope.user_library_read

        with self.subTest('Returns scope'):
            self.assertIsInstance(s, Scope)

        with self.subTest('Returns first operand'):
            self.assertEqual(str(s), 'user-read-private')

    def test_subtracting_same_scope_returns_empty(self):
        s = scope.user_library_read - scope.user_library_read
        self.assertSetEqual(s, set())

    def test_adding_other_than_scopes_returns_not_implemented(self):
        r = scope.user_library_read.__add__(1)
        self.assertIs(r, NotImplemented)

    def test_subtracting_other_than_scopes_returns_not_implemented(self):
        r = scope.user_library_read.__sub__(1)
        self.assertIs(r, NotImplemented)


class TestScope(unittest.TestCase):
    def test_repr_like_instantiation(self):
        s = Scope('a', 'b')
        self.assertEqual(repr(s), "Scope('a', 'b')")

    def test_empty_scope_equal_to_empty_set(self):
        s = Scope()
        self.assertSetEqual(s, set())

    def test_scope_initialisable_with_strings(self):
        s = Scope('b', 'a')
        self.assertEqual(str(s), 'a b')

    def test_scope_initialisable_with_enum(self):
        s = Scope(scope.user_read_private)
        self.assertEqual(str(s), 'user-read-private')

    def test_scope_initialisable_with_combination(self):
        s = Scope('a', 'b', scope.user_read_private)
        self.assertEqual(str(s), 'a b user-read-private')

    def test_different_object_same_str_results_in_no_duplicates(self):
        s = Scope(scope.user_read_private, 'user-read-private')
        self.assertSetEqual(s, {'user-read-private'})

    def test_scope_unpackable(self):
        s1 = Scope('b', 'a')
        s2 = Scope(*s1)
        self.assertSetEqual(s1, s2)

    def test_adding_scopes(self):
        s1 = Scope('b', 'a')
        s2 = Scope('c', 'b')

        with self.subTest('Returns scope'):
            self.assertIsInstance(s1 + s2, Scope)

        with self.subTest('Results in union'):
            self.assertSetEqual(s1 + s2, {'a', 'b', 'c'})

        with self.subTest('LHS retained'):
            self.assertEqual(str(s1), 'a b')

        with self.subTest('RHS retained'):
            self.assertEqual(str(s2), 'b c')

    def test_adding_str_successful(self):
        s1 = Scope('b', 'a')
        s2 = 'c'
        self.assertSetEqual(s1 + s2, {'a', 'b', 'c'})

    def test_adding_authorisation_scope_successful(self):
        s1 = Scope('a')
        s2 = scope.user_read_private
        self.assertSetEqual(s1 + s2, {'user-read-private', 'a'})

    def test_r_adding_str_successful(self):
        s1 = 'c'
        s2 = Scope('b', 'a')
        self.assertSetEqual(s1 + s2, {'a', 'b', 'c'})

    def test_r_adding_authorisation_scope_successful(self):
        s1 = scope.user_read_private
        s2 = Scope('a')
        self.assertSetEqual(s1 + s2, {'user-read-private', 'a'})

    def test_adding_unsupported_raises_not_implemented(self):
        s = Scope('user-read-private', 'a')
        with self.assertRaises(NotImplementedError):
            s + 1

    def test_subtracting_scopes(self):
        s1 = Scope('b', 'a')
        s2 = Scope('c', 'b')

        with self.subTest('Returns scope'):
            self.assertIsInstance(s1 - s2, Scope)

        with self.subTest('Results in relative complement'):
            self.assertSetEqual(s1 - s2, {'a'})

        with self.subTest('LHS retained'):
            self.assertEqual(str(s1), 'a b')

        with self.subTest('RHS retained'):
            self.assertEqual(str(s2), 'b c')

    def test_subtracting_str_successful(self):
        s1 = Scope('b', 'a')
        s2 = 'b'
        self.assertSetEqual(s1 - s2, {'a'})

    def test_subtracting_authorisation_scope_successful(self):
        s1 = Scope('user-read-private', 'a')
        s2 = scope.user_read_private
        self.assertSetEqual(s1 - s2, {'a'})

    def test_r_subtracting_str_successful(self):
        s1 = 'b'
        s2 = Scope('b', 'a')
        self.assertSetEqual(s1 - s2, set())

    def test_r_subtracting_authorisation_scope_successful(self):
        s1 = scope.user_read_private
        s2 = Scope('user-read-private', 'a')
        self.assertSetEqual(s1 - s2, set())

    def test_subtracting_unsupported_raises_not_implemented(self):
        s = Scope('user-read-private', 'a')
        with self.assertRaises(NotImplementedError):
            s - 1

    def test_r_subtracting_unsupported_raises_not_implemented(self):
        s = Scope('user-read-private', 'a')
        with self.assertRaises(NotImplementedError):
            1 - s
