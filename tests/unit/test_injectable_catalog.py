import unittest

from tests.sdk import assert_contains, assert_contains_all

from kanata import find_injectables
from kanata.catalogs import InjectableCatalog
from .test_injectables import ITransient1, Singleton, Transient1

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

        registrations = find_injectables("tests.unit.test_injectables")
        catalog = InjectableCatalog(registrations)
        result = catalog.get_registrations_by_contract(ITransient1)
        self.assertIsNotNone(result)
        assert_contains(result, lambda i: i.injectable_type in [Singleton, Transient1])

if __name__ == "__main__":
    unittest.main()
