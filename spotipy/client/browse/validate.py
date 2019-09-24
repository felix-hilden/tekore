recommendation_prefixes = {'min', 'max', 'target'}
recommendation_attributes = {
    'acousticness',
    'danceability',
    'duration_ms',
    'energy',
    'instrumentalness',
    'key',
    'liveness',
    'loudness',
    'mode',
    'popularity',
    'speechiness',
    'tempo',
    'time_signature',
    'valence'
}


def is_valid(attribute: str) -> bool:
    """
    Determine if a recommendation attribute is valid.

    Parameters
    ----------
    attribute
        attribute name

    Returns
    -------
    bool
        validity
    """
    if '_' not in attribute:
        return False

    p, a = attribute.split('_')

    if p not in recommendation_prefixes or a not in recommendation_attributes:
        return False

    return True


def validate_attributes(attributes: dict) -> None:
    """
    Validate recommendation attributes.

    Raise ValueError if any attribute is not allowed.

    Parameters
    ----------
    attributes
        recommendation attributes
    """
    for name in attributes:
        if not is_valid(name):
            raise ValueError(f'Invalid attribute `{name}`!')
