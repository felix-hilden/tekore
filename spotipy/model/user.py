from typing import List
from dataclasses import dataclass

from spotipy.model.base import Item
from spotipy.model.member import Followers, Image


@dataclass
class User(Item):
    display_name: str
    external_urls: dict
    followers: Followers = None
    images: List[Image] = None

    def __post_init__(self):
        if self.followers is not None:
            self.followers = Followers(**self.followers)
        if self.images is not None:
            self.images = [Image(**i) for i in self.images]


@dataclass
class PrivateUser(User):
    country: str = None
    email: str = None
    product: str = None


@dataclass
class PublicUser(User):
    pass
