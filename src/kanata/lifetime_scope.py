from collections.abc import Iterable
from typing import Any

import structlog

from kanata.catalogs import IInjectableCatalog
from kanata.utils import get_dependent_contracts
from .constants import LOGGER_NAME
from .exceptions import DependencyResolutionException
from .graphs import BidirectedGraph
from .graphs.sorting import topological_sort
from .ilifetime_scope import ILifetimeScope, TInjectable
from .models import (
    InjectableInstanceRegistration, InjectableRegistration, InjectableScopeType,
    InjectableTypeRegistration, InstanceCollection
)
from .resolvers import DefaultResolver, IResolver

class LifetimeScope(ILifetimeScope):
    """An injectable lifetime scope
    that manages the lifetimes of injectables
    and provides access to them."""

    def __init__(
        self,
        catalog: IInjectableCatalog,
        resolvers: tuple[IResolver, ...] | None = None,
        _parent: ILifetimeScope | None = None
    ) -> None:
        self.__catalog = catalog
        self.__resolvers: tuple[IResolver, ...] = resolvers or (DefaultResolver(),)
        self.__parent = _parent
        self.__log = structlog.get_logger(logger_name=LOGGER_NAME)
        self.__instances = InstanceCollection()

    def resolve(self, injectable: type[TInjectable]) -> TInjectable:
        if self.__parent and self.__should_resolve_via_parent(injectable):
            return self.__parent.resolve(injectable)

        dependency_graph = self.__build_dependency_graph_for(injectable)
        instance = None
        for current_injectable in topological_sort(dependency_graph, injectable):
            self.__log.debug("Resolving injectable", type=current_injectable)
            instance = self.__resolve_injectable(current_injectable)
            self.__log.debug("Resolved injectable", type=current_injectable)

        if not isinstance(instance, injectable):
            raise DependencyResolutionException(
                type(instance),
                (
                    "Got an unexpected type during dependency resolution."
                    " This is likely an error in the algorithm."
                )
            )

        return instance

    def create_child_scope(self) -> ILifetimeScope:
        return LifetimeScope(self.__catalog, self.__resolvers, _parent=self)

    def __build_dependency_graph_for(self, injectable: type) -> BidirectedGraph[type]:
        graph: BidirectedGraph[type] = BidirectedGraph()
        injectables_to_resolve: list[type] = [injectable]
        while injectables_to_resolve:
            dependee_injectable = injectables_to_resolve.pop()
            if not graph.try_add_node(dependee_injectable):
                # This type's dependency chain has already been mapped.
                continue

            self.__log.debug("Gathering dependent contracts", dependee=dependee_injectable)
            dependent_contracts = get_dependent_contracts(dependee_injectable)
            for dependent_contract, is_multi in dependent_contracts:
                self.__log.debug(
                    "Found dependent contract",
                    dependee=dependee_injectable,
                    dependent=dependent_contract,
                    is_multi=is_multi
                )
                dependent_registrations = self.__catalog.get_registrations_by_contract(
                    dependent_contract)
                if len(dependent_registrations) == 0 and not is_multi:
                    raise DependencyResolutionException(
                        dependee_injectable,
                        "Cannot satisfy the dependency"
                        f" of {dependee_injectable} on {dependent_contract}."
                    )

                injectables_to_resolve.extend(
                    self.__mark_dependent_types(
                        graph,
                        dependee_injectable,
                        dependent_registrations
                    )
                )

        return graph

    def __resolve_injectable(self, injectable: type) -> Any:
        registration = self.__catalog.get_registration_by_injectable(injectable)
        if not registration:
            raise DependencyResolutionException(
                injectable,
                f"Cannot find the registration for injectable '{injectable}'."
                " It is possible that this type is not an injectable."
            )

        # For singleton and scoped injectables, we know that there exists one and only one
        # instance for all of the associated contracts, therefore we can find and return
        # that specific one if it is created already.
        if isinstance(registration, InjectableInstanceRegistration):
            return registration.injectable_instance
        if not isinstance(registration, InjectableTypeRegistration):
            raise DependencyResolutionException(
                type(registration),
                "Unsupported type of injectable registration."
            )

        if (
            registration.scope in (InjectableScopeType.SINGLETON, InjectableScopeType.SCOPED)
            and (instances := self.__instances.get_instances_by_contract(
                injectable,
                registration.scope
            ))
            and (instance := next(iter(instances), None))
        ):
            return instance

        for resolver in self.__resolvers:
            instance = resolver.resolve(
                self.__catalog,
                self.__instances,
                injectable,
                registration.scope
            )
            if not instance:
                continue

            self.__log.debug("Instantiated injectable", injectable=injectable)
            self.__instances.add_instance(registration.scope, injectable, instance)
            return instance

        raise DependencyResolutionException(
            injectable,
            "None of the resolvers could resolve an instance of the specified type."
        )

    def __should_resolve_via_parent(
        self,
        injectable: type
    ) -> bool:
        registration = self.__catalog.get_registration_by_injectable(injectable)
        match registration:
            case InjectableTypeRegistration(scope=InjectableScopeType.SINGLETON): return True
            case InjectableInstanceRegistration(): return True
            case _: return False

    def __mark_dependent_types(
        self,
        graph: BidirectedGraph[type],
        dependee_injectable: type,
        dependent_registrations: Iterable[InjectableRegistration]
    ) -> Iterable[type]:
        # Mark each implementation as a dependency. At this point,
        # it is possible only one of them will be needed by
        # this specific type. But we'll make sure all are initialized
        # as they may be needed later.
        dependent_types = []
        for dependent_registration in dependent_registrations:
            match dependent_registration:
                case InjectableTypeRegistration():
                    injectable_type = dependent_registration.injectable_type
                case InjectableInstanceRegistration():
                    injectable_type = type(dependent_registration.injectable_instance)
                case _:
                    raise DependencyResolutionException(
                        type(dependent_registration),
                        "Unsupported type of injectable registration."
                    )

            graph.try_add_node(dependee_injectable)
            graph.try_add_edge(dependee_injectable, injectable_type)
            dependent_types.append(injectable_type)
            self.__log.debug(
                "Identified dependent injectable",
                dependee=dependee_injectable,
                dependent=injectable_type
            )
        return dependent_types
