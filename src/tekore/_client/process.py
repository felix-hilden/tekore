from __future__ import annotations

from collections.abc import Callable

from tekore.model import Model


def nothing(json: dict) -> dict:
    """Pass value without doing anything."""
    return json


def top_item(item: str) -> Callable:
    """Return ``item`` from top level of dict."""

    def post_func(json: dict) -> dict:
        return json[item]

    return post_func


def single(type_: type[Model], from_item: str | None = None) -> Callable:
    """
    Unpack dict or items in ``from_item`` into single constructor.

    If dict or ``from_item`` is None - does nothing and returns None.
    """

    def post_func(json: dict) -> Model | None:
        json = json if from_item is None else json[from_item]
        return type_(**json) if json is not None else None

    return post_func


def model_list(type_: type[Model], from_item: str | None = None) -> Callable:
    """Unpack items inside ``from_item`` of dict into constructors."""

    def post_func(json: dict) -> list[Model | None]:
        json = json if from_item is None else json[from_item]
        return [type_(**i) if i is not None else None for i in json]

    return post_func


def multiple(*args: Callable) -> Callable:
    """Run json dict through multiple processors."""

    def post_func(json: dict) -> tuple:
        return tuple(processor(json) for processor in args)

    return post_func
