from tekore._error import get_error, errors, ClientError, ServerError


class TestGetError:
    def test_known_error_retrieved(self):
        """
        Test if the given error occurs.

        Args:
            self: (todo): write your description
        """
        status = 400
        assert get_error(status) is errors[status]

    def test_unknown_client_error(self):
        """
        Test if the client error.

        Args:
            self: (todo): write your description
        """
        status = 499
        assert get_error(status) is ClientError

    def test_unknown_server_error(self):
        """
        Test if the server is raised.

        Args:
            self: (todo): write your description
        """
        status = 599
        assert get_error(status) is ServerError
