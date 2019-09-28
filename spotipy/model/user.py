from typing import List
from dataclasses import dataclass

from spotipy.model.base import Item
from spotipy.model.member import Followers, Image


@dataclass
class User(Item):
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
    explicit_content: bool = None
    country: str = None
    email: str = None
    product: str = None


@dataclass
class PublicUser(User):
    pass
