import pytest

from tekore import Sender, SyncSender


class TestSender:
    def test_sender_cannot_be_instantiated(self):
        with pytest.raises(TypeError):
            Sender()

    def test_repr(self):
        s = SyncSender()
        assert repr(s).startswith("SyncSender(")
