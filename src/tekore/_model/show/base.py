from typing import List, Optional, Union

from pydantic import Field

from ..base import Item
from ..member import Copyright, Image


class Show(Item):
    """
    Show base.

    :attr:`publisher` being an object is undocumented.
    """

    available_markets: List[str] = Field(default_factory=list)
    copyrights: List[Copyright]
    description: str
    explicit: bool
    external_urls: dict
    html_description: Optional[str] = None
    images: List[Image]
    is_externally_hosted: Optional[bool]
    languages: List[str]
    media_type: str
    name: str
    publisher: Union[str, dict]
    total_episodes: Optional[int] = None
