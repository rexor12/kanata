from .models import InjectableRegistration
from abc import ABCMeta, abstractmethod
from typing import Any, Iterable, Optional, Type, TypeVar

T = TypeVar("T")

class IInjectableCatalog(metaclass=ABCMeta):
    """Interface for a catalog of injectable registrations."""

    @abstractmethod
    def get_registrations(self) -> Iterable[InjectableRegistration]:
        """Gets all the registrations available in the catalog.

        :return: The available registrations.
        :rtype: Iterable[InjectableRegistration]
        """

    @abstractmethod
    def get_registrations_by_contract(
        self,
        contract: Type[Any]) -> Iterable[InjectableRegistration]:
        """Gets the registrations associated to the specified contract.

        :param contract: The contract for which to get the registrations.
        :type contract: Type[Any]
        :return: The registrations associated to the contract.
        :rtype: Iterable[InjectableRegistration]
        """

    @abstractmethod
    def get_registration_by_injectable(
        self,
        injectable: Type[Any]) -> Optional[InjectableRegistration]:
        """Gets the registration associated to the specified injectable.

        :param injectable: The injectable for which to get the registration.
        :type injectable: Type[Any]
        :return: If exists, the registration associated to the injectable.
        :rtype: Optional[InjectableRegistration]
        """
