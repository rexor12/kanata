from dataclasses import dataclass

from .injectable_registration import InjectableRegistration
from .injectable_scope_type import InjectableScopeType

@dataclass(kw_only=True)
class InjectableTypeRegistration(InjectableRegistration):
    """Holds information about the registration of an injectable type."""

    injectable_type: type
    """Gets or sets the type of the injectable object."""

    scope: InjectableScopeType = InjectableScopeType.TRANSIENT
    """Gets or sets the lifetime scope type of the created instances."""
