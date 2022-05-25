from .test_injectables import (
    CaptiveDependency, MissingMultipleDependencies, MissingSingleDependency,
    Singleton, Root, Transient1, Transient2
)
from kanata import InjectableCatalog, LifetimeScope, find_injectables
from kanata.exceptions import DependencyResolutionException
from kanata.models import LifetimeScopeOptions
from tests.sdk import assert_contains, assert_contains_unique

import unittest

class LifetimeScopeTests(unittest.TestCase):
    """Unit tests for lifetime scopes."""

    def test_resolve_should_resolve_single_injectable(self):
        """Asserts that a type is resolved correctly."""

        registrations = find_injectables("tests.unit.test_injectables")
        catalog = InjectableCatalog(registrations)
        scope = LifetimeScope(catalog)

        instance = scope.resolve(Transient1)

        self.assertIsNotNone(instance)

    def test_resolve_singleton_twice_should_resolve_single_injectable(self):
        """Asserts that a single instance is returned
        when a singleton is resolved multiple times.
        """

        registrations = find_injectables("tests.unit.test_injectables")
        catalog = InjectableCatalog(registrations)
        scope = LifetimeScope(catalog)

        instance1 = scope.resolve(Singleton)
        instance2 = scope.resolve(Singleton)

        self.assertIsNotNone(instance1)
        self.assertIsNotNone(instance2)
        self.assertEqual(instance1, instance2)

    def test_resolve_transient_twice_should_resolve_two_injectables(self):
        """Asserts that two different instances are returned
        when a transient is resolved multiple times.
        """

        registrations = find_injectables("tests.unit.test_injectables")
        catalog = InjectableCatalog(registrations)
        scope = LifetimeScope(catalog)

        instance1 = scope.resolve(Transient1)
        instance2 = scope.resolve(Transient1)

        self.assertIsNotNone(instance1)
        self.assertIsNotNone(instance2)
        self.assertNotEqual(instance1, instance2)

    def test_resolve_should_raise_with_single_instance_dependency_missing(self):
        """Asserts that an injectable that has a single instance dependency
        raises an exception when no such instance exists.
        """

        registrations = find_injectables("tests.unit.test_injectables")
        catalog = InjectableCatalog(registrations)
        scope = LifetimeScope(catalog)

        self.assertRaises(
            DependencyResolutionException,
            lambda: scope.resolve(MissingSingleDependency))

    def test_resolve_should_raise_with_singleton_captive_dependency(self):
        """Asserts that a singleton injectable that has a transient dependency
        raises an exception with the default options.
        """

        registrations = find_injectables("tests.unit.test_injectables")
        catalog = InjectableCatalog(registrations)
        scope = LifetimeScope(catalog)

        self.assertRaises(DependencyResolutionException, lambda: scope.resolve(CaptiveDependency))

    def test_resolve_should_resolve_with_singleton_captive_dependency_when_permitted(self):
        """Asserts that a singleton injectable that has a transient dependency
        resolves just fine when permitted via the lifetime scope options.
        """

        registrations = find_injectables("tests.unit.test_injectables")
        options = LifetimeScopeOptions(raise_on_captive_dependency=False)
        catalog = InjectableCatalog(registrations)
        scope = LifetimeScope(catalog, options)

        instance = scope.resolve(CaptiveDependency)

        self.assertIsNotNone(instance)

    def test_resolve_should_resolve_with_multi_instance_dependency_missing(self):
        """Asserts that an injectable that has a multi-instance dependency
        is resolved correctly when no such instance exists.
        """

        registrations = find_injectables("tests.unit.test_injectables")
        catalog = InjectableCatalog(registrations)
        scope = LifetimeScope(catalog)

        instance = scope.resolve(MissingMultipleDependencies)

        self.assertIsNotNone(instance)

    def test_resolve_should_resolve_dependencies_correctly(self):
        """Asserts that a type and its dependencies are resolved correctly."""

        registrations = find_injectables("tests.unit.test_injectables")
        catalog = InjectableCatalog(registrations)
        scope = LifetimeScope(catalog)

        instance = scope.resolve(Root)

        self.assertIsNotNone(instance)
        self.assertEqual(len(instance.injectables1), 2)
        self.assertEqual(len(instance.injectables2), 2)
        assert_contains_unique(instance.injectables1, type)
        assert_contains_unique(instance.injectables2, type)
        # Disable the type check because here we want to verify
        # that the types are exactly these.
        # pylint: disable=unidiomatic-typecheck
        assert_contains(instance.injectables1, lambda i: type(i) == Transient1)
        assert_contains(instance.injectables1, lambda i: type(i) == Singleton)
        assert_contains(instance.injectables2, lambda i: type(i) == Transient2)
        assert_contains(instance.injectables2, lambda i: type(i) == Singleton)
        # pylint: enable=unidiomatic-typecheck

if __name__ == "__main__":
    unittest.main()