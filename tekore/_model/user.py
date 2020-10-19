from typing import List, Optional
from dataclasses import dataclass

from .base import Item
from .member import Followers, Image
from .serialise import Model, ModelList


@dataclass(repr=False)
class ExplicitContent(Model):
    """Explicit content filter of a user."""

    filter_enabled: bool
    filter_locked: bool


@dataclass(repr=False)
class User(Item):
    """
    User base.

    :attr:`display_name`, :attr:`followers` and :attr:`images`
    may not be available.
    """

    external_urls: dict
    display_name: Optional[str] = None
    followers: Optional[Followers] = None
    images: Optional[List[Image]] = None

    def __post_init__(self):
        if self.followers is not None:
            self.followers = Followers(**self.followers)
        if self.images is not None:
            self.images = ModelList(Image(**i) for i in self.images)


@dataclass(repr=False)
class PrivateUser(User):
    """
    User with private information.

    :attr:`country`, :attr:`explicit_content` and :attr:`product`
    require the ``user-read-private`` scope.
    :attr:`email` requires the ``user-read-email`` scope.
    :attr:`birthday` is unavailable unless the now-invalid
    ``user-read-birthdate`` scope was granted to the token.
    """

    country: Optional[str] = None
    email: Optional[str] = None
    explicit_content: Optional[ExplicitContent] = None
    product: Optional[str] = None
    birthday: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        if self.explicit_content is not None:
            self.explicit_content = ExplicitContent(**self.explicit_content)


@dataclass(repr=False)
class PublicUser(User):
    """User as viewable by anyone."""
