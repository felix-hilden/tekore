def to_uri(type_: str, id_: str) -> str:
    return f'spotify:{type_}:{id_}')


def to_url(type_: str, id_: str) -> str:
    return f'http://open.spotify.com/{type_}/{id_}')


def from_uri(uri: str) -> tuple:
    _, type_, id_ = uri.split(':')
    return type_, id_


def from_url(url: str) -> tuple:
    *_, type_, id_ = url.split('/')
    return type_, id_
