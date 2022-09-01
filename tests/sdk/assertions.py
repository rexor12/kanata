"""Contains additional assertions."""

from collections.abc import Callable, Iterable
from typing import Any, TypeVar

T = TypeVar("T")

def assert_contains(iterable: Iterable[T], predicate: Callable[[T], bool]) -> None:
    """Asserts that the specified iterable has at least one
    item that matches the specified predicate.

    :param iterable: The source iterable.
    :type iterable: Iterable[T]
    :param predicate: A predicate that determines a match.
    :type predicate: Callable[[T], bool]
    :raises AssertionError: Raised when no matching element is found.
    """

    for item in iterable:
        if predicate(item):
            return
    raise AssertionError((
        "Expected the list to contain an item matching the specified predicate,"
        " but it wasn't found."
    ))

def assert_contains_all(iterable: Iterable[T], items: Iterable[T]) -> None:
    """Asserst that the specified iterable contains all of the specified items.

    :param iterable: The source iterable.
    :type iterable: Iterable[T]
    :param items: The items needed to be contained by the iterable.
    :type items: Iterable[T]
    :raises AssertionError: Raised when one or more of the items aren't contained by the iterable.
    """

    for item in items:
        if item not in iterable:
            raise AssertionError((
                "Expected the list to contain all items,"
                " but some weren't found."
            ))

def assert_contains_unique(iterable: Iterable[T], projection: Callable[[T], Any]) -> None:
    """Asserts that the specified iterable only contains unique items.

    :param iterable: The source iterable.
    :type iterable: Iterable[T]
    :param projection: A projection used for the comparison.
    :type projection: Callable[[T], Any]
    :raises AssertionError: Raised when the iterable has one or more duplicate items.
    """

    checked_items: set[Any] = set()
    for item in iterable:
        projected_item = projection(item)
        if projected_item in checked_items:
            raise AssertionError((
                "Expected the list to only contain unique items,"
                " but found duplicate values."
            ))
        checked_items.add(projected_item)
