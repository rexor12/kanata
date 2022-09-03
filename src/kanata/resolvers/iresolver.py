from typing import Protocol, TypeVar

from kanata.catalogs import IInjectableCatalog
from kanata.models import IInstanceCollection, InjectableScopeType

TInjectable = TypeVar("TInjectable")

class IResolver(Protocol):
    """Interface for a service that can resolve instances of injectables."""

    def resolve(
        self,
        catalog: IInjectableCatalog,
        instances: IInstanceCollection,
        injectable: type[TInjectable],
        scope_type: InjectableScopeType
    ) -> TInjectable:
        """Resolves an instance of a specific injectable.

        :param catalog: The catalog of injectables.
        :type catalog: IInjectableCatalog
        :param instances: The already resolved instances of injectables.
        :type instances: IInstanceCollection
        :param injectable: The type of the injectable to be resolved.
        :type injectable: type[TInjectable]
        :param scope_type: The scope for which to resolve the injectable.
        :type scope_type: InjectableScopeType
        :return: The resolved injectable instance.
        :rtype: TInjectable
        """
        ...
