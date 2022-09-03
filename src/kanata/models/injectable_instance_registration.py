from dataclasses import dataclass
from typing import Any

from .injectable_registration import InjectableRegistration

@dataclass(kw_only=True)
class InjectableInstanceRegistration(InjectableRegistration):
    injectable_instance: Any
    """Gets or sets the injectable instance."""
