"""Utility methods for types."""

from collections.abc import Callable
from typing import Any, TypeVar

TAttribute = TypeVar("TAttribute")

def get_or_add_attribute(
    clazz: type[Any],
    name: str,
    default_factory: Callable[[], TAttribute]
) -> TAttribute:
    """Gets the attribute with the specified name, if exists;
    otherwise adds it with the value determined by the specified value factory.

    :param clazz: The type of the class.
    :type clazz: type[Any]
    :param name: The name of the attribute.
    :type name: str
    :param default_factory: A value factory for the default value to add, if needed.
    :type default_factory: Callable[[], TAttribute]
    :return: The value of the attribute.
    :rtype: TAttribute
    """

    attribute: TAttribute | None = getattr(clazz, name, None)
    if attribute is None:
        attribute = default_factory()
        setattr(clazz, name, attribute)
    return attribute
