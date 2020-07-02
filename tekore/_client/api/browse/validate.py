from itertools import product
from tekore.model import RecommendationAttribute

prefixes = {'min', 'max', 'target'}
attributes = set(str(a) for a in RecommendationAttribute)
valid = set('_'.join(i) for i in product(prefixes, attributes))


def validate_attributes(candidates: dict) -> None:
    """
    Validate recommendation attributes.

    Parameters
    ----------
    candidates
        recommendation attributes to validate

    Raises
    ------
    ValueError
        if any attribute is not allowed
    """
    for name in candidates:
        if name not in valid:
            raise ValueError(f'Invalid attribute `{name}`!')
