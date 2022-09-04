import unittest
from typing import cast

from tests.sdk import assert_contains, assert_contains_all

from kanata import find_injectables
from kanata.catalogs import InjectableCatalog, InjectableCatalogBuilder
from kanata.models import InjectableInstanceRegistration, InjectableTypeRegistration
from .test_injectables import ISingleton, ITransient1, Singleton, Transient1

class _TestInstanceService(ISingleton):
    pass

class _TestTransientService(Transient1):
    pass

class InjectableCatalogTests(unittest.TestCase):
    """Unit tests for InjectableCatalog."""

    def test_get_registrations_should_return_all_registrations(self):
        """Asserts that the catalog returns all registrations."""

        registrations = find_injectables("tests.unit.test_injectables")
        catalog = InjectableCatalog(registrations)
        assert_contains_all(catalog.get_registrations(), registrations)

    def test_get_registration_by_injectable_should_have_all_contracts(self):
        """Asserts that the registration returned by the catalog
        contains all contracts.
        """

        registrations = find_injectables("tests.unit.test_injectables")
        catalog = InjectableCatalog(registrations)
        registration = catalog.get_registration_by_injectable(Singleton)
        self.assertIsNotNone(registration)
        # Ignored the type, because Pylance doesn't recognize
        # contract_types as a field (possibly a dataclass related bug).
        self.assertEqual(len(registration.contract_types), 3) # type: ignore

    def test_get_registrations_by_contract_should_return_all_matching_registrations(self):
        """Asserts that the catalog returns all registrations
        associated to a specified contract.
        """

        instance = _TestInstanceService()
        catalog_builder = InjectableCatalogBuilder()
        (catalog_builder
            .add_module("tests.unit.test_injectables")
            .register_instance(instance, (ISingleton,))
            .register_type(_TestTransientService, (ITransient1,))
        )
        catalog = catalog_builder.build()

        result = catalog.get_registrations_by_contract(ITransient1)
        self.assertIsNotNone(result)
        type_registrations = map(
            lambda i: cast(InjectableTypeRegistration, i),
            filter(lambda i: isinstance(i, InjectableTypeRegistration), result)
        )
        assert_contains(type_registrations, lambda i: i.injectable_type is Singleton)
        assert_contains(type_registrations, lambda i: i.injectable_type is Transient1)
        assert_contains(type_registrations, lambda i: i.injectable_type is _TestTransientService)

        result = catalog.get_registrations_by_contract(ISingleton)
        instance_registrations = map(
            lambda i: cast(InjectableInstanceRegistration, i),
            filter(lambda i: isinstance(i, InjectableInstanceRegistration), result)
        )
        assert_contains(instance_registrations, lambda i: isinstance(i.injectable_instance, _TestInstanceService))

if __name__ == "__main__":
    unittest.main()
