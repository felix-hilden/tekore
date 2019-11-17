from typing import List
from dataclasses import dataclass

from spotipy.serialise import SerialisableDataclass
from spotipy.model.base import Item
from spotipy.model.member import Followers, Image


@dataclass
class ExplicitContent(SerialisableDataclass):
    filter_enabled: bool
    filter_locked: bool


@dataclass
class User(Item):
    """
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
            self.images = [Image(**i) for i in self.images]


@dataclass
class PrivateUser(User):
    """
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


@dataclass
class PublicUser(User):
    pass
