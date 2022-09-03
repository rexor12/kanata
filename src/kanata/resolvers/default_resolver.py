from typing import TypeVar

import structlog

from kanata.catalogs import IInjectableCatalog
from kanata.constants import LOGGER_NAME
from kanata.exceptions import DependencyResolutionException
from kanata.models import IInstanceCollection, InjectableScopeType
from .default_resolver_options import DefaultResolverOptions
from .resolver_base import ResolverBase

TInjectable = TypeVar("TInjectable")

class DefaultResolver(ResolverBase):
    """Default implementation of a resolver."""

    def __init__(
        self,
        options: DefaultResolverOptions | None = None
    ) -> None:
        super().__init__()
        self.__options = options or DefaultResolverOptions()
        self.__log = structlog.get_logger(logger_name=LOGGER_NAME)

    def resolve(
        self,
        catalog: IInjectableCatalog,
        instances: IInstanceCollection,
        injectable: type[TInjectable],
        scope_type: InjectableScopeType
    ) -> TInjectable:
        return injectable(*self._get_dependencies(catalog, instances, injectable, scope_type))

    def _on_captive_dependency_detected(
        self,
        injectable: type,
        contract: type
    ) -> None:
        # Unless turned off, issue a warning, because a captive dependency
        # may be the result of a coding error, as it's generally undesirable.
        error_message = (
            "Detected captive dependency."
            f" Singleton '{injectable}' depends on transient '{contract}'."
        )
        if not self.__options.suppress_captive_dependency_warnings:
            self.__log.warn(error_message)
        if self.__options.raise_on_captive_dependency:
            raise DependencyResolutionException(injectable, error_message)
