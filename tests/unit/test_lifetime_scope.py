import unittest
from typing import TypeVar

from tests.sdk import assert_contains, assert_contains_unique

from kanata import LifetimeScope, find_injectables
from kanata.catalogs import InjectableCatalog
from kanata.exceptions import DependencyResolutionException
from kanata.resolvers import DefaultResolver, DefaultResolverOptions
from .test_injectables import (
    MissingMultipleDependencies, MissingSingleDependency, ProtocolDependent, ProtocolImpl, Root,
    Scoped, ScopedToTransientDependency, Singleton, SingletonToScopedDependency,
    SingletonToTransientDependency, Transient1, Transient2
)

TInjectable = TypeVar("TInjectable")

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

    def test_resolve_should_raise_with_singleton_to_transient_dependency(self):
        """Asserts that a singleton injectable that has a transient dependency
        raises an exception with the default options.
        """

        registrations = find_injectables("tests.unit.test_injectables")
        catalog = InjectableCatalog(registrations)
        scope = LifetimeScope(catalog)

        self.assertRaises(
            DependencyResolutionException,
            lambda: scope.resolve(SingletonToTransientDependency)
        )

    def test_resolve_should_raise_with_singleton_to_scoped_dependency(self):
        """Asserts that a singleton injectable that has a scoped dependency
        raises an exception with the default options.
        """

        registrations = find_injectables("tests.unit.test_injectables")
        catalog = InjectableCatalog(registrations)
        scope = LifetimeScope(catalog)

        self.assertRaises(
            DependencyResolutionException,
            lambda: scope.resolve(SingletonToScopedDependency)
        )

    def test_resolve_should_raise_with_scoped_to_transient_dependency(self):
        """Asserts that a scoped injectable that has a transient dependency
        raises an exception with the default options.
        """

        registrations = find_injectables("tests.unit.test_injectables")
        catalog = InjectableCatalog(registrations)
        scope = LifetimeScope(catalog)

        self.assertRaises(
            DependencyResolutionException,
            lambda: scope.resolve(ScopedToTransientDependency)
        )

    def test_resolve_should_resolve_with_singleton_to_transient_dependency_when_permitted(self):
        """Asserts that a singleton injectable that has a transient dependency
        resolves just fine when permitted via the lifetime scope options.
        """

        registrations = find_injectables("tests.unit.test_injectables")
        options = DefaultResolverOptions(raise_on_captive_dependency=False)
        catalog = InjectableCatalog(registrations)
        scope = LifetimeScope(catalog, (DefaultResolver(options),))

        instance = scope.resolve(SingletonToTransientDependency)

        self.assertIsNotNone(instance)

    def test_resolve_should_resolve_with_singleton_to_scoped_dependency_when_permitted(self):
        """Asserts that a singleton injectable that has a scoped dependency
        resolves just fine when permitted via the lifetime scope options.
        """

        registrations = find_injectables("tests.unit.test_injectables")
        options = DefaultResolverOptions(raise_on_captive_dependency=False)
        catalog = InjectableCatalog(registrations)
        scope = LifetimeScope(catalog, (DefaultResolver(options),))

        instance = scope.resolve(SingletonToScopedDependency)

        self.assertIsNotNone(instance)

    def test_resolve_should_resolve_with_scoped_to_transient_dependency_when_permitted(self):
        """Asserts that a scoped injectable that has a transient dependency
        resolves just fine when permitted via the lifetime scope options.
        """

        registrations = find_injectables("tests.unit.test_injectables")
        options = DefaultResolverOptions(raise_on_captive_dependency=False)
        catalog = InjectableCatalog(registrations)
        scope = LifetimeScope(catalog, (DefaultResolver(options),))

        instance = scope.resolve(ScopedToTransientDependency)

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

    def test_resolve_scoped_injectable_twice_returns_the_same_instance(self):
        """Asserts that the child lifetime scope creates a new instance of a scoped injectable."""

        registrations = find_injectables("tests.unit.test_injectables")
        catalog = InjectableCatalog(registrations)
        scope = LifetimeScope(catalog)

        scoped1 = scope.resolve(Scoped)
        scoped2 = scope.resolve(Scoped)

        self.assertEqual(scoped1, scoped2)

    def test_resolve_of_child_scope_returns_the_same_singleton_as_parent(self):
        """Asserts that the child lifetime scope returns the same instance
        of a singleton as the parent lifetime scope."""

        registrations = find_injectables("tests.unit.test_injectables")
        catalog = InjectableCatalog(registrations)
        parent_scope = LifetimeScope(catalog)
        child_scope = parent_scope.create_child_scope()

        parent_singleton = parent_scope.resolve(Singleton)
        child_singleton = child_scope.resolve(Singleton)

        self.assertEqual(parent_singleton, child_singleton)

    def test_resolve_of_child_scope_returns_different_scoped_instance_than_parent(self):
        """Asserts that the child lifetime scope creates a new instance of a scoped injectable."""

        registrations = find_injectables("tests.unit.test_injectables")
        catalog = InjectableCatalog(registrations)
        parent_scope = LifetimeScope(catalog)
        child_scope = parent_scope.create_child_scope()

        parent_scoped = parent_scope.resolve(Scoped)
        child_scoped = child_scope.resolve(Scoped)

        self.assertNotEqual(parent_scoped, child_scoped)

    def test_resolve_should_resolve_by_protocol(self):
        """Asserts that the lifetime scope correctly resolves a type
        that implements a protocol.
        """

        registrations = find_injectables("tests.unit.test_injectables")
        catalog = InjectableCatalog(registrations)
        scope = LifetimeScope(catalog)

        instance = scope.resolve(ProtocolDependent)

        self.assertIsNotNone(instance)
        self.assertIsInstance(instance, ProtocolDependent)
        self.assertIsInstance(instance.injected, ProtocolImpl)

if __name__ == "__main__":
    unittest.main()
