from collections.abc import Generator
from typing import Any, Protocol

from .injectable_scope_type import InjectableScopeType

class IInstanceCollection(Protocol):
    """Interface for a resolved instance collection."""

    def get_instances_by_contract(
        self,
        contract_type: type,
        scope_type: InjectableScopeType | None = None
    ) -> Generator[Any, None, None]:
        ...
