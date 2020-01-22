from typing import Optional, Callable

from tekore.serialise import ModelList


def nothing(json):
    """
    Pass value without doing anything.
    """
    return json


def top_item(item: str):
    """
    Return ``item`` from top level of dict.
    """
    def post_func(json: dict):
        return json[item]
    return post_func


def single(type_: type, top_item: Optional[str] = None):
    """
    Unpack dict or items in ``top_item`` into single constructor.
    If dict or ``top_item`` is None - does nothing and returns None.
    """
    def post_func(json: dict):
        json = json if top_item is None else json[top_item]
        return type_(**json) if json is not None else None
    return post_func


def single_or_dict(type_: type):
    """
    Tries to unpack dict into single constructor returning untouched dict if failed.
    """
    def post_func(json: dict):
        try:
            return type_(**json)
        except TypeError:
            return json

    return post_func


def model_list(type_: type, top_item: Optional[str] = None):
    """
    Unpack items inside ``top_item`` of dict into constructors.
    """
    def post_func(json: dict):
        json = json if top_item is None else json[top_item]
        return ModelList(type_(**i) if i is not None else None for i in json)
    return post_func


def multiple(*args: Callable):
    """
    Run json dict through multiple processors.
    """
    def post_func(json: dict):
        return (processor(json) for processor in args)
    return post_func
