import pytest
from tekore import Sender, SyncSender


class TestSender:
    def test_sender_cannot_be_instantiated(self):
        """
        : parameter_test_instantiated.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(TypeError):
            Sender()

    def test_repr(self):
        """
        Test if a test is a test case.

        Args:
            self: (todo): write your description
        """
        s = SyncSender()
        assert repr(s).startswith('SyncSender(')
