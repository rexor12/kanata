"""Utility methods for types."""

import inspect
from collections.abc import Callable, Generator
from typing import TypeVar, get_args

from kanata.exceptions import DependencyResolutionException

TAttribute = TypeVar("TAttribute")

def get_or_add_attribute(
    clazz: type,
    name: str,
    default_factory: Callable[[], TAttribute]
) -> TAttribute:
    """Gets the attribute with the specified name, if exists;
    otherwise adds it with the value determined by the specified value factory.

    :param clazz: The type of the class.
    :type clazz: type
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

def get_dependent_contracts(
    injectable: type) -> Generator[tuple[type, bool], None, None]:
    constructor = getattr(injectable, "__init__", None)
    if not constructor or not callable(constructor):
        raise DependencyResolutionException(injectable, "Invalid constructor.")
    signature = inspect.signature(constructor)
    for name, descriptor in signature.parameters.items():
        if name in ("self", "args", "kwargs"):
            continue
        if descriptor.annotation == inspect.Parameter.empty:
            raise DependencyResolutionException(
                injectable,
                f"The initializer of '{injectable}' is missing annotations."
            )
        yield __unpack_dependent_intf(descriptor.annotation)

def __unpack_dependent_intf(contract: type) -> tuple[type, bool]:
    if (
        getattr(contract, "_is_protocol", False) # typing.Protocol
        or getattr(contract, "__abstractmethods__", None) # abc.ABCMeta
        or (origin := getattr(contract, "__origin__", None)) is None
    ):
        return (contract, False)

    if origin is not tuple:
        raise DependencyResolutionException(
            contract,
            f"Expected a tuple, but got {origin} for contract {contract}."
        )

    args = get_args(contract)
    if len(args) != 2 or args[-1] != Ellipsis:
        raise DependencyResolutionException(
            contract,
            "Expected a tuple with two arguments, the second being an ellipsis."
        )
    return (args[0], True)
