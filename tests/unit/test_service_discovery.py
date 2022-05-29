from kanata import find_injectables
from tests.sdk import assert_contains_all, first
from tests.unit.test_injectables import (
    INonDependee, IRoot, IScoped, ISingleton, ITransient1, ITransient2, CaptiveScopedDependency,
    CaptiveTransientDependency, MissingMultipleDependencies, MissingSingleDependency,
    Root, Scoped, Singleton, Transient1, Transient2
)
from typing import Any, Dict, Tuple, Type

import unittest

class ServiceDiscoveryTests(unittest.TestCase):
    """Unit tests for service discovery."""

    def test_find_injectables_should_find_all_injectables_recursively(self):
        """Asserts that all injectables are discovered in a specific module."""

        expected_types: Dict[Type[Any], Tuple[Type[Any], ...]] = {
            Root: (IRoot,),
            Singleton: (ITransient1, ITransient2, ISingleton),
            Transient1: (ITransient1,),
            Transient2: (ITransient2,),
            MissingMultipleDependencies: (INonDependee,),
            MissingSingleDependency: (INonDependee,),
            CaptiveScopedDependency: (INonDependee,),
            CaptiveTransientDependency: (INonDependee,),
            Scoped: (IScoped,)
        }

        registrations = find_injectables("tests.unit.test_injectables")

        self.assertEqual(len(registrations), len(expected_types))
        for injectable, contracts in expected_types.items():
            registration = first(registrations, lambda i, t=injectable: i.injectable_type == t)
            self.assertEqual(len(contracts), len(registration.contract_types))
            assert_contains_all(registration.contract_types, contracts)

if __name__ == "__main__":
    unittest.main()
