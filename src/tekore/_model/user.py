from __future__ import annotations

from .base import Item
from .member import Followers, Image
from .serialise import Model


class ExplicitContent(Model):
    """Explicit content filter of a user."""

    filter_enabled: bool
    filter_locked: bool


class User(Item):
    """
    User base.

    :attr:`display_name`, :attr:`followers` and :attr:`images`
    may not be available.
    """

    external_urls: dict
    display_name: str | None = None
    followers: Followers | None = None
    images: list[Image] | None = None


class PrivateUser(User):
    """
    User with private information.

    :attr:`country`, :attr:`explicit_content` and :attr:`product`
    require the ``user-read-private`` scope.
    :attr:`email` requires the ``user-read-email`` scope.
    :attr:`birthday` is unavailable unless the now-invalid
    ``user-read-birthdate`` scope was granted to the token.
    """

    country: str | None = None
    email: str | None = None
    explicit_content: ExplicitContent | None = None
    product: str | None = None
    birthday: str | None = None


class PublicUser(User):
    """User as viewable by anyone."""
