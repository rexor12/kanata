"""Utility methods for iterables."""

from collections.abc import Callable, Iterable
from typing import Any, TypeVar

T = TypeVar("T")

def all_true(iterable: Iterable[T], predicate: Callable[[T], bool]) -> bool:
    """Determines whether the specified predicate is True
    for all items of the specified iterable.

    :param iterable: The source iterable.
    :type iterable: Iterable[T]
    :param predicate: A predicate that determines the truthfulness of an item.
    :type predicate: Callable[[T], bool]
    :return: True, if and only if the predicate is True for all items.
    :rtype: bool
    """

    return all(predicate(item) for item in iterable)

def first(iterable: Iterable[T], predicate: Callable[[T], bool], **kwargs: Any) -> T:
    """Gets the first item from the specified iterable that
    matches the specified predicate.

    :param iterable: The source iterable.
    :type iterable: Iterable[T]
    :param predicate: The predicate used to determine a match.
    :type predicate: Callable[[T], bool]
    :raises ValueError: Raised when there is no matching item.
    :return: The first item that matches the specified predicate.
    :rtype: T
    """

    for item in iterable:
        if predicate(item):
            return item

    if "default" in kwargs:
        return kwargs["default"]

    raise ValueError("There is no matching item the predicate.")
