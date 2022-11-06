from tekore._sender.error import get_error, errors, ClientError, ServerError


class TestGetError:
    def test_known_error_retrieved(self):
        status = 400
        assert get_error(status) is errors[status]

    def test_unknown_client_error(self):
        status = 499
        assert get_error(status) is ClientError

    def test_unknown_server_error(self):
        status = 599
        assert get_error(status) is ServerError
