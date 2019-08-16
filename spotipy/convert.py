def to_uri(type_: str, id_: str) -> str:
    return 'spotify:{}:{}'.format(type_, id_)


def to_url(type_: str, id_: str) -> str:
    return 'http://open.spotify.com/{}/{}'.format(type_, id_)


def from_uri(uri: str) -> tuple:
    _, type_, id_ = uri.split(':')
    return type_, id_


def from_url(url: str) -> tuple:
    *_, type_, id_ = url.split('/')
    return type_, id_
