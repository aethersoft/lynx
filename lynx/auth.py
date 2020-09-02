import typing

from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth, MultiAuth


class Auth:
    def __init__(self):
        """Creates access control class for authentication and authorization."""
        self._basic_auth = HTTPBasicAuth()
        self._token_auth = HTTPTokenAuth()
        self._auth = MultiAuth(self._basic_auth, self._token_auth)
        self._resources = {}

    def error_handler(self, f: typing.Callable) -> typing.NoReturn:
        """Set error handler for Authentication Errors.

        :param f: error handler.
        :return: NoReturn
        """
        self._token_auth.error_handler(f)
        self._basic_auth.error_handler(f)

    def verify_password(self, f: typing.Callable) -> typing.Any:
        """ Verifies basic password.

        :param f: function defining verification process.
        :return: Any
        """
        return self._basic_auth.verify_password(f)

    def verify_token(self, f: typing.Callable) -> typing.Any:
        """ Verifies token.

        :param f: function defining verification process.
        :return: Any
        """
        return self._token_auth.verify_token(f)

    def login_required(self, f: typing.Callable = None, role: typing.Text = None) -> typing.Any:
        """ Identifies as login required for provided function {f}.

        :param f: input function.
        :param role: user role
        :return: func
        """
        return self._auth.login_required(f, role)
