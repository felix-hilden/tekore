from unittest import TestCase
from tekore import scope, Scope


class TestScopesEnum(TestCase):
    def test_str_is_enum_value(self):
        s = scope.user_read_private
        self.assertEqual(str(s), 'user-read-private')

    def test_subtracting_same_scope_returns_empty(self):
        s = scope.user_library_read - scope.user_library_read
        self.assertSetEqual(s, set())


class TestScope(TestCase):
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

    def test_adding_scopes_preserves_originals(self):
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

    def test_subtracting_scopes_preservers_originals(self):
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


class TestScopeOperations(TestCase):
    def test_add_invalid_scope(self):
        with self.assertRaises(NotImplementedError):
            1 + scope.user_top_read

    def test_add_invalid_Scope(self):
        with self.assertRaises(NotImplementedError):
            1 + Scope('a')

    def test_add_str_scope(self):
        s = 'a' + scope.user_top_read
        self.assertEqual(str(s), 'a user-top-read')

    def test_add_str_Scope(self):
        s = 'a' + Scope('b')
        self.assertEqual(str(s), 'a b')

    def test_add_scope_str(self):
        s = scope.user_top_read + 'a'
        self.assertEqual(str(s), 'a user-top-read')

    def test_add_scope_scope(self):
        s = scope.user_follow_read + scope.user_top_read
        self.assertEqual(str(s), 'user-follow-read user-top-read')

    def test_add_scope_Scope(self):
        s = scope.user_top_read + Scope('a')
        self.assertEqual(str(s), 'a user-top-read')

    def test_add_scope_invalid_raises(self):
        with self.assertRaises(NotImplementedError):
            scope.user_top_read + 1

    def test_add_Scope_str(self):
        s = Scope('a') + 'b'
        self.assertEqual(str(s), 'a b')

    def test_add_Scope_scope(self):
        s = Scope('a') + scope.user_top_read
        self.assertEqual(str(s), 'a user-top-read')

    def test_add_Scope_Scope(self):
        s = Scope('a') + Scope('b')
        self.assertEqual(str(s), 'a b')

    def test_add_Scope_invalid_raises(self):
        with self.assertRaises(NotImplementedError):
            Scope('a') + 1

    def test_sub_invalid_scope(self):
        with self.assertRaises(NotImplementedError):
            1 - scope.user_top_read

    def test_sub_invalid_Scope(self):
        with self.assertRaises(NotImplementedError):
            1 - Scope('a')

    def test_sub_str_scope_different(self):
        s = 'a' - scope.user_top_read
        self.assertEqual(str(s), 'a')

    def test_sub_str_scope_same(self):
        s = 'user-top-read' - scope.user_top_read
        self.assertEqual(str(s), '')

    def test_sub_str_Scope_different(self):
        s = 'a' - Scope('b')
        self.assertEqual(str(s), 'a')

    def test_sub_str_Scope_same(self):
        s = 'a' - Scope('a')
        self.assertEqual(str(s), '')

    def test_sub_scope_str_different(self):
        s = scope.user_top_read - 'a'
        self.assertEqual(str(s), 'user-top-read')

    def test_sub_scope_str_same(self):
        s = scope.user_top_read - 'user-top-read'
        self.assertEqual(str(s), '')

    def test_sub_scope_scope_different(self):
        s = scope.user_top_read - scope.user_follow_read
        self.assertEqual(str(s), 'user-top-read')

    def test_sub_scope_scope_same(self):
        s = scope.user_top_read - scope.user_top_read
        self.assertEqual(str(s), '')

    def test_sub_scope_Scope_different(self):
        s = scope.user_top_read - Scope('a')
        self.assertEqual(str(s), 'user-top-read')

    def test_sub_scope_Scope_same(self):
        s = scope.user_top_read - Scope('user-top-read')
        self.assertEqual(str(s), '')

    def test_sub_scope_invalid_raises(self):
        with self.assertRaises(NotImplementedError):
            scope.user_top_read - 1

    def test_sub_Scope_str_different(self):
        s = Scope('a') - 'b'
        self.assertEqual(str(s), 'a')

    def test_sub_Scope_str_same(self):
        s = Scope('a') - 'a'
        self.assertEqual(str(s), '')

    def test_sub_Scope_scope_different(self):
        s = Scope('a') - scope.user_top_read
        self.assertEqual(str(s), 'a')

    def test_sub_Scope_scope_same(self):
        s = Scope('user-top-read') - scope.user_top_read
        self.assertEqual(str(s), '')

    def test_sub_Scope_Scope_different(self):
        s = Scope('a') - Scope('b')
        self.assertEqual(str(s), 'a')

    def test_sub_Scope_Scope_same(self):
        s = Scope('a') - Scope('a')
        self.assertEqual(str(s), '')

    def test_sub_Scope_invalid_raises(self):
        with self.assertRaises(NotImplementedError):
            Scope('a') - 1
