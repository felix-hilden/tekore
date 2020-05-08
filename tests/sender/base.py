import pytest
from tekore import Sender


class TestSender:
    def test_sender_cannot_be_instantiated(self):
        with pytest.raises(TypeError):
            Sender()
