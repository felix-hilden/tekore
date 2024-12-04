from __future__ import annotations

from .serialise import Model, StrEnum


class ReleaseDatePrecision(StrEnum):
    """Precision of a release date."""

    year = "year"
    month = "month"
    day = "day"
    minute = "minute"


class Copyright(Model):
    """Copyright."""

    text: str
    type: str


class Followers(Model):
    """
    Followers.

    :attr:`href` is always ``None``.
    """

    href: None
    total: int


class Image(Model):
    """
    Image link and information.

    The Web API documentation reports that :attr:`height` and :attr:`width`
    can be ``None`` or not available in the response.
    """

    url: str
    height: int | None
    width: int | None


class Restrictions(Model):
    """Restrictions on relinked resource."""

    reason: str


class ResumePoint(Model):
    """Resume point."""

    fully_played: bool
    resume_position_ms: int
