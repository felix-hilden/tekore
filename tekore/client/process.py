from typing import Callable
from tekore.serialise import ModelList


def nothing(json):
    """
    Pass value without doing anything.
    """
    return json


def top_item(item: str) -> Callable:
    """
    Return ``item`` from top level of dict.
    """
    def post_func(json: dict):
        return json[item]
    return post_func


def single(type_: type, from_item: str = None) -> Callable:
    """
    Unpack dict or items in ``from_item`` into single constructor.
    If dict or ``from_item`` is None - does nothing and returns None.
    """
    def post_func(json: dict):
        json = json if from_item is None else json[from_item]
        return type_(**json) if json is not None else None
    return post_func


def single_or_dict(type_: type) -> Callable:
    """
    Try to unpack dict into single constructor returning untouched dict if failed.
    """
    def post_func(json: dict):
        try:
            return type_(**json)
        except TypeError:
            return json

    return post_func


def model_list(type_: type, from_item: str = None) -> Callable:
    """
    Unpack items inside ``from_item`` of dict into constructors.
    """
    def post_func(json: dict):
        json = json if from_item is None else json[from_item]
        return ModelList(type_(**i) if i is not None else None for i in json)
    return post_func


def multiple(*args: Callable):
    """
    Run json dict through multiple processors.
    """
    def post_func(json: dict):
        return (processor(json) for processor in args)
    return post_func
