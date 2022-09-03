from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from kanata import find_injectables
from kanata.models import (
    InjectableInstanceRegistration, InjectableRegistration, InjectableScopeType,
    InjectableTypeRegistration
)
from .iinjectable_catalog import IInjectableCatalog
from .injectable_catalog import InjectableCatalog

class InjectableCatalogBuilder:
    """An injectable catalog builder."""

    def __init__(self) -> None:
        self.__registrations = list[InjectableRegistration]()

    def add_module(self, module_name: str) -> InjectableCatalogBuilder:
        """Discovers the injectable registrations from the module with the specified name.

        :param module_name: The name of the module to explore.
        :type module_name: str
        :return: The same instance of the builder.
        :rtype: InjectableCatalogBuilder
        """

        self.__registrations.extend(find_injectables(module_name))
        return self

    def register_instance(
        self,
        instance: Any,
        contract_types: Iterable[type]
    ) -> InjectableCatalogBuilder:
        """Registers the specified instance as an injectable.

        :param instance: The instance to be registered.
        :type instance: Any
        :param contract_types: The contracts by which to register the instance.
        :type contract_types: Iterable[type]
        :return: The same instance of the builder.
        :rtype: InjectableCatalogBuilder
        """

        # TODO https://github.com/PyCQA/pylint/issues/6550
        self.__registrations.append(
            InjectableInstanceRegistration( # pylint: disable=unexpected-keyword-arg
                contract_types=set(contract_types),
                injectable_instance=instance
            )
        )
        return self

    def register_type(
        self,
        injectable_type: type,
        contract_types: Iterable[type],
        scope_type: InjectableScopeType = InjectableScopeType.TRANSIENT
    ) -> InjectableCatalogBuilder:
        """Registers the specified type as an injectable.

        :param injectable_type: The type to be registered.
        :type injectable_type: type
        :param contract_types: The contracts by which to register the type.
        :type contract_types: Iterable[type]
        :param scope_type: The injectable scope, defaults to InjectableScopeType.TRANSIENT
        :type scope_type: InjectableScopeType, optional
        :return: The same instance of the builder.
        :rtype: InjectableCatalogBuilder
        """

        # TODO https://github.com/PyCQA/pylint/issues/6550
        self.__registrations.append(
            InjectableTypeRegistration( # pylint: disable=unexpected-keyword-arg
                contract_types=set(contract_types),
                injectable_type=injectable_type,
                scope=scope_type
            )
        )
        return self

    def build(self) -> IInjectableCatalog:
        """Builds the injectable catalog.

        :return: The new instance of the injectable catalog.
        :rtype: IInjectableCatalog
        """

        return InjectableCatalog(self.__registrations)
