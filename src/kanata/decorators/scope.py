from collections.abc import Callable
from typing import TypeVar

from kanata.models import InjectableRegistration, InjectableScopeType
from kanata.utils import get_or_add_attribute

T = TypeVar("T")

def scope(scope_type: InjectableScopeType) -> Callable[[type[T]], type[T]]:
    """Specifies the scope type of an injectable class.

    :param scope_type: The lifetime scope of the created instances.
    :type scope_type: InjectableScopeType, optional
    :return: A decorator that returns the same class that it decorates.
    :rtype: Callable[[type[T]], type[T]]
    """
    def decorator(wrapped_class: type[T]) -> type[T]:
        registration = get_or_add_attribute(
            wrapped_class,
            InjectableRegistration.PROPERTY_NAME,
            lambda: InjectableRegistration(wrapped_class))
        registration.scope = scope_type
        return wrapped_class

    return decorator
