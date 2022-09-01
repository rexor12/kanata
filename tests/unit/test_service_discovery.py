import unittest
from typing import Any

from tests.sdk import assert_contains_all, first
from tests.unit.test_injectables import (
    INonDependee, IRoot, IScoped, ISingleton, ITransient1, ITransient2, MissingMultipleDependencies,
    MissingSingleDependency, ProtocolDependent, ProtocolImpl, ProtocolInterface, Root, Scoped,
    ScopedToTransientDependency, Singleton, SingletonToScopedDependency,
    SingletonToTransientDependency, Transient1, Transient2
)

from kanata import find_injectables

class ServiceDiscoveryTests(unittest.TestCase):
    """Unit tests for service discovery."""

    def test_find_injectables_should_find_all_injectables_recursively(self):
        """Asserts that all injectables are discovered in a specific module."""

        expected_types: dict[type[Any], tuple[type[Any], ...]] = {
            Root: (IRoot,),
            Singleton: (ITransient1, ITransient2, ISingleton),
            Transient1: (ITransient1,),
            Transient2: (ITransient2,),
            MissingMultipleDependencies: (INonDependee,),
            MissingSingleDependency: (INonDependee,),
            Scoped: (IScoped,),
            ScopedToTransientDependency: (INonDependee,),
            SingletonToScopedDependency: (INonDependee,),
            SingletonToTransientDependency: (INonDependee,),
            ProtocolImpl: (ProtocolInterface,),
            ProtocolDependent: (INonDependee,)
        }

        registrations = find_injectables("tests.unit.test_injectables")

        self.assertEqual(len(registrations), len(expected_types))
        for injectable, contracts in expected_types.items():
            registration = first(registrations, lambda i, t=injectable: i.injectable_type == t)
            self.assertEqual(len(contracts), len(registration.contract_types))
            assert_contains_all(registration.contract_types, contracts)

if __name__ == "__main__":
    unittest.main()
