from typing import List
from dataclasses import dataclass

from .base import Item
from .member import Followers, Image
from .serialise import Model, ModelList


@dataclass(repr=False)
class ExplicitContent(Model):
    """
    Explicit content filter of a user.
    """
    filter_enabled: bool
    filter_locked: bool


@dataclass(repr=False)
class User(Item):
    """
    User base.

    Display name, followers and images may not be available.
    """
    external_urls: dict
    display_name: str = None
    followers: Followers = None
    images: List[Image] = None

    def __post_init__(self):
        if self.followers is not None:
            self.followers = Followers(**self.followers)
        if self.images is not None:
            self.images = ModelList(Image(**i) for i in self.images)


@dataclass(repr=False)
class PrivateUser(User):
    """
    User with private information.

    Country, explicit content and product require user-read-private scope.
    Email requires user-read-email scope.
    """
    country: str = None
    email: str = None
    explicit_content: ExplicitContent = None
    product: str = None

    def __post_init__(self):
        super().__post_init__()
        if self.explicit_content is not None:
            self.explicit_content = ExplicitContent(**self.explicit_content)


@dataclass(repr=False)
class PublicUser(User):
    """
    User as viewable by anyone.
    """
