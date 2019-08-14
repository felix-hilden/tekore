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


@dataclass
class PrivateUser(User):
    country: str
    email: str
    product: str


@dataclass
class PublicUser(User):
    pass
