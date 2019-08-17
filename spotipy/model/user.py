from typing import List
from dataclasses import dataclass

from spotipy.model.base import Item
from spotipy.model.member import Followers, Image


@dataclass
class User(Item):
    display_name: str
    external_urls: dict
    followers: Followers
    images: List[Image]

    def __post_init__(self):
        self.followers = Followers(**self.followers)
        self.images = [Image(**i) for i in self.images]


@dataclass
class PrivateUser(User):
    country: str
    email: str
    product: str


@dataclass
class PublicUser(User):
    pass
