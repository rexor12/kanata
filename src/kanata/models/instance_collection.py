from collections.abc import Generator
from typing import Any

from .iinstance_collection import IInstanceCollection
from .injectable_scope_type import InjectableScopeType

class InstanceCollection(IInstanceCollection):
    def __init__(self) -> None:
        self.__instances = dict[InjectableScopeType, dict[type, set]]()

    def get_instances_by_contract(
        self,
        contract_type: type,
        scope_type: InjectableScopeType | None = None
    ) -> Generator[Any, None, None]:
        if scope_type is None:
            for injectables_by_contract in self.__instances.values():
                for instance in injectables_by_contract.get(contract_type, ()):
                    yield instance
            return

        if not (injectables_by_contract := self.__instances.get(scope_type)):
            return

        for instance in injectables_by_contract.get(contract_type, tuple()):
            yield instance

    def add_instance(
        self,
        scope_type: InjectableScopeType,
        injectable_type: type,
        instance: Any
    ) -> None:
        if not (instances_by_scope := self.__instances.get(scope_type)):
            self.__instances[scope_type] = instances_by_scope = {}
        if not (instances := instances_by_scope.get(injectable_type)):
            instances_by_scope[injectable_type] = instances = set()
        instances.add(instance)
