from typing import Callable
from tekore.model import ModelList, Model


def nothing(json):
    """Pass value without doing anything."""
    return json


def top_item(item: str) -> Callable:
    """Return ``item`` from top level of dict."""
    def post_func(json: dict):
        return json[item]
    return post_func


def single(type_: Model, from_item: str = None) -> Callable:
    """
    Unpack dict or items in ``from_item`` into single constructor.

    If dict or ``from_item`` is None - does nothing and returns None.
    """
    def post_func(json: dict):
        json = json if from_item is None else json[from_item]
        return type_.from_kwargs(json) if json is not None else None
    return post_func


def model_list(type_: Model, from_item: str = None) -> Callable:
    """Unpack items inside ``from_item`` of dict into constructors."""
    def post_func(json: dict):
        json = json if from_item is None else json[from_item]
        return ModelList(type_.from_kwargs(i) if i is not None else None for i in json)
    return post_func


def multiple(*args: Callable):
    """Run json dict through multiple processors."""
    def post_func(json: dict):
        return tuple(processor(json) for processor in args)
    return post_func
