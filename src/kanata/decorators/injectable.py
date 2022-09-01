from collections.abc import Callable
from typing import Any, TypeVar

from kanata.models import InjectableRegistration
from kanata.utils import get_or_add_attribute

T = TypeVar("T")

def injectable(contract_type: type[Any]) -> Callable[[type[T]], type[T]]:
    """Marks a class as an injectable.

    :param contract_type: The type of the contract by which an instance of the object is injectable.
    :type contract_type: type[Any]
    :return: A decorator that returns the same class that it decorates.
    :rtype: Callable[[type[T]], type[T]]
    """

    def decorator(wrapped_class: type[T]) -> type[T]:
        registration = get_or_add_attribute(
            wrapped_class,
            InjectableRegistration.PROPERTY_NAME,
            lambda: InjectableRegistration(wrapped_class))
        registration.contract_types.add(contract_type)
        return wrapped_class

    return decorator
