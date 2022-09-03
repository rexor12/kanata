from dataclasses import dataclass

from .injectable_registration import InjectableRegistration
from .injectable_scope_type import InjectableScopeType

@dataclass(kw_only=True)
class InjectableTypeRegistration(InjectableRegistration):
    injectable_type: type
    """Gets or sets the type of the injectable object."""

    scope: InjectableScopeType = InjectableScopeType.TRANSIENT
    """Gets or sets the lifetime scope type of the created instances."""
