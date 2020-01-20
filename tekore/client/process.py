from tekore.serialise import ModelList


def nothing(json):
    """
    Pass value without doing anything.
    """
    return json


def single(type_: type):
    """
    Unpack dict into single constructor.
    """
    def post_func(json: dict):
        return type_(**json)
    return post_func


def model_list(type_: type, top_item: str):
    """
    Unpack items inside ``top_item`` of dict into constructors.
    """
    def post_func(json: dict):
        return ModelList(type_(**i) for i in json[top_item])
    return post_func
