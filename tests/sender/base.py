from unittest import TestCase
from tekore import Sender


class TestSender(TestCase):
    def test_sender_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Sender()
