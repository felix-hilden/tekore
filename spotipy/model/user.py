from typing import List
from dataclasses import dataclass

from spotipy.model.base import Item
from spotipy.model.member import ExternalURL, Followers, Image


@dataclass
class User(Item):
    display_name: str
    external_urls: ExternalURL
    followers: Followers
    images: List[Image]

    def __post_init__(self):
        self.external_urls = ExternalURL(**self.external_urls)
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
