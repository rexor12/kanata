from abc import ABC, abstractmethod
from typing import Any, TypeVar

from kanata.catalogs import IInjectableCatalog
from kanata.exceptions import DependencyResolutionException
from kanata.models import IInstanceCollection, InjectableScopeType
from kanata.utils import get_dependent_contracts
from .iresolver import IResolver

TInjectable = TypeVar("TInjectable")

_SCOPE_TYPE_RANKS: dict[InjectableScopeType, int] = {
    InjectableScopeType.TRANSIENT: 0,
    InjectableScopeType.SCOPED: 1,
    InjectableScopeType.SINGLETON: 2
}

class ResolverBase(ABC, IResolver):
    """Abstract base class for a resolver."""

    @abstractmethod
    def resolve(
        self,
        catalog: IInjectableCatalog,
        instances: IInstanceCollection,
        injectable: type[TInjectable],
        scope_type: InjectableScopeType
    ) -> TInjectable:
        ...

    @staticmethod
    def _is_captive_dependency(
        dependee_scope: InjectableScopeType,
        dependent_scope: InjectableScopeType
    ) -> bool:
        """Determines if the dependee and dependent scopes
        result in a captive dependency.

        :param dependee_scope: The scope of the dependee.
        :type dependee_scope: InjectableScopeType
        :param dependent_scope: The scope of the dependent.
        :type dependent_scope: InjectableScopeType
        :return: True, if a captive dependency is detected.
        :rtype: bool
        """

        ranked_scopes = sorted(
            (dependee_scope, dependent_scope),
            key=lambda i: _SCOPE_TYPE_RANKS[i]
        )
        return ranked_scopes[0] != dependee_scope

    def _on_captive_dependency_detected(
        self,
        injectable: type,
        contract: type
    ) -> None:
        """Invoked when a captive dependency is detected
        so that the resolver can handle the situation.

        This method should be overridden by subclasses
        and it does nothing by default.

        :param injectable: The type of the causing injectable.
        :type injectable: type
        :param contract: The type of the dependent contract.
        :type contract: type
        """

    def _get_dependencies(
        self,
        catalog: IInjectableCatalog,
        instances: IInstanceCollection,
        injectable: type,
        dependee_scope: InjectableScopeType
    ) -> list[Any]:
        """Gets the dependencies of the specified injectable.

        :param catalog: The catalog of injectables.
        :type catalog: IInjectableCatalog
        :param instances: The already resolved instances of injectables.
        :type instances: IInstanceCollection
        :param injectable: The type of the injectable for which to get the dependencies.
        :type injectable: type
        :param dependee_scope: The scope of the dependee.
        :type dependee_scope: InjectableScopeType
        :raises DependencyResolutionException: Raised when a dependency cannot be satisfied.
        :return: The list of dependencies.
        :rtype: list[Any]
        """

        dependent_contracts = get_dependent_contracts(injectable)
        dependent_injectables = []
        for dependent_contract, is_multi in dependent_contracts:
            registrations = catalog.get_registrations_by_contract(dependent_contract)
            candidate_instances = []
            for registration in registrations:
                if ResolverBase._is_captive_dependency(dependee_scope, registration.scope):
                    self._on_captive_dependency_detected(injectable, dependent_contract)

                candidate_instances.extend(
                    instances.get_instances_by_contract(
                        registration.injectable_type,
                        registration.scope
                    )
                )

            if is_multi:
                dependent_injectables.append(tuple(candidate_instances))
            elif len(candidate_instances) > 0:
                dependent_injectables.append(candidate_instances[0])
            else:
                raise DependencyResolutionException(
                    injectable,
                    (
                        "Cannot satisfy the dependency"
                        f"of '{injectable}' on '{dependent_contract}'."
                    )
                )
        return dependent_injectables
