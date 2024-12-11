from __future__ import annotations

import operator
from collections.abc import Callable, Generator
from functools import reduce, wraps

from .base import SpotifyBase


def _chunks(lst: list, n: int, *, reverse: bool) -> Generator[list]:
    """
    Chunk list into length 'n' sublists.

    Parameters
    ----------
    lst
        list to chunk
    n
        length of chunks
    reverse
        reverse the order of chunks
    """
    rng = range(0, len(lst), n)

    if reverse:
        rng = rng[::-1]

    for i in rng:
        yield lst[i : i + n]


def _get_arg(position: int, name: str, args, kwargs):
    """Get argument from args or kwargs."""
    return kwargs.get(name, None) if len(args) <= position else args[position]


def _replace_arg(position: int, name: str, value, args, kwargs):
    if len(args) <= position:
        kwargs[name] = value
    else:
        args = args[:position] + (value,) + args[position + 1 :]
    return args, kwargs


def chunked(  # noqa: C901
    arg_name: str,
    arg_pos: int,
    chunk_size: int,
    process: Callable,
    reverse: str | None = None,
    reverse_pos: int | None = None,
    chain: str | None = None,
    chain_pos: int | None = None,
) -> Callable:
    """
    Decorate a function to make multiple calls splitting a list argument.

    Optionally chain the return value of the previous request
    to the specified variable in the next request.

    Parameters
    ----------
    arg_name
        argument to chunk
    arg_pos
        index of argument in the argument list
    chunk_size
        size of chunk to send at a time
    process
        process response list
    reverse
        reverse order of chunks sent when argument defined
    reverse_pos
        position of the reverse argument
    chain
        variable to chain into the next request
    chain_pos
        position of the chain argument
    """

    def decorator(function: Callable) -> Callable:  # noqa: C901
        nonlocal arg_pos, reverse_pos, chain_pos
        arg_pos -= 1
        if reverse_pos is not None:
            reverse_pos -= 1
        if chain_pos is not None:
            chain_pos -= 1

        def replace(arg_val, chain_val, args, kwargs):
            args, kwargs = _replace_arg(arg_pos, arg_name, arg_val, args, kwargs)

            if chain is not None:
                args, kwargs = _replace_arg(chain_pos, chain, chain_val, args, kwargs)

            return args, kwargs

        async def async_wrapper(self: SpotifyBase, chunks, chain_val, args, kwargs):
            responses = []
            for chunk in chunks:
                args, kwargs = replace(chunk, chain_val, args, kwargs)
                chain_val = await function(self, *args, **kwargs)
                responses.append(chain_val)

            return process(responses)

        @wraps(function)
        def wrapper(self: SpotifyBase, *args, **kwargs):
            arg_val = _get_arg(arg_pos, arg_name, args, kwargs)
            if not self.chunked_on or arg_val is None:
                return function(self, *args, **kwargs)

            if chain is not None:
                chain_val = _get_arg(chain_pos, chain, args, kwargs)
            else:
                chain_val = None

            if reverse is not None:
                reverse_val = _get_arg(reverse_pos, reverse, args, kwargs)
                reverse_bool = reverse_val is not None
            else:
                reverse_bool = False

            chunks = _chunks(arg_val, chunk_size, reverse=reverse_bool)

            if self.is_async:
                return async_wrapper(self, chunks, chain_val, args, kwargs)

            responses = []
            for chunk in chunks:
                args, kwargs = replace(chunk, chain_val, args, kwargs)
                chain_val = function(self, *args, **kwargs)
                responses.append(chain_val)

            return process(responses)

        return wrapper

    return decorator


def join_lists(responses: list):
    """Join lists of models."""
    return reduce(operator.iadd, responses, [])


def return_none(_: list) -> None:
    """Return None always."""
    return


def return_last(responses: list):
    """Return last item of a list."""
    return responses[-1] if responses else None
