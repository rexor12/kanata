from collections.abc import Iterable
from typing import Any

from kanata.utils import get_or_add
from .iinjectable_catalog import IInjectableCatalog
from .models import InjectableRegistration

class InjectableCatalog(IInjectableCatalog):
    """Provides access to information about the known injectables."""

    def __init__(self, registrations: Iterable[InjectableRegistration]) -> None:
        self.__registrations_by_contract: dict[type[Any], list[InjectableRegistration]] = {}
        self.__registrations_by_injectable: dict[type[Any], InjectableRegistration] = {}
        self.__build_registration_maps(registrations)

    def get_registrations(self) -> tuple[InjectableRegistration, ...]:
        return tuple(self.__registrations_by_injectable.values())

    def get_registrations_by_contract(
        self,
        contract: type[Any]) -> tuple[InjectableRegistration, ...]:
        return tuple(self.__registrations_by_contract.get(contract, []))

    def get_registration_by_injectable(
        self,
        injectable: type[Any]) -> InjectableRegistration | None:
        return self.__registrations_by_injectable.get(injectable, None)

    def __build_registration_maps(self, registrations: Iterable[InjectableRegistration]) -> None:
        for registration in registrations:
            for contract_type in registration.contract_types:
                by_injectables: list[InjectableRegistration] = get_or_add(
                    self.__registrations_by_contract,
                    contract_type,
                    lambda _: [])
                by_injectables.append(registration)

            self.__registrations_by_injectable[registration.injectable_type] = registration
