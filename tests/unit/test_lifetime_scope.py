import unittest
from typing import Any, Generic, Protocol, TypeVar

from tests.sdk import assert_contains, assert_contains_unique

from kanata import LifetimeScope, find_injectables
from kanata.catalogs import InjectableCatalog, InjectableCatalogBuilder
from kanata.exceptions import DependencyResolutionException
from kanata.models import InjectableRegistration, InjectableScopeType
from kanata.resolvers import DefaultResolver, DefaultResolverOptions, IResolver, ResolverContext
from .test_injectables import (
    MissingMultipleDependencies, MissingSingleDependency, ProtocolDependent, ProtocolImpl, Root,
    Scoped, ScopedToTransientDependency, Singleton, SingletonToScopedDependency,
    SingletonToTransientDependency, Transient1, Transient2
)

TInjectable = TypeVar("TInjectable")

class _ITestService:
    pass

class _TestInstanceService(_ITestService):
    pass

class _InstanceDependent:
    def __init__(
        self,
        test_service: _ITestService
    ) -> None:
        self.test_service = test_service

_TGeneric = TypeVar("_TGeneric", covariant=True)

class _IGeneric(Protocol[_TGeneric]):
    @property
    def value(self) -> _TGeneric:
        ...

class _GenericImpl(Generic[_TGeneric], _IGeneric[_TGeneric]):
    @property
    def value(self) -> _TGeneric:
        return self.__value

    @property
    def generic_type_argument(self) -> type:
        raise NotImplementedError

    def __init__(self, test_service: _ITestService) -> None:
        super().__init__()
        self.test_service = test_service
        self.__value = self.generic_type_argument()

class _GenericImpl2(Generic[_TGeneric], _IGeneric[_TGeneric]):
    @property
    def value(self) -> _TGeneric:
        raise NotImplementedError

class _GenericTypeArg1:
    pass

class _GenericTypeArg2:
    pass

class _RootWithDifferentGenericDependencies:
    def __init__(
        self,
        generic1: _IGeneric[_GenericTypeArg1],
        generic2: _IGeneric[_GenericTypeArg2]
    ) -> None:
        self.generic1 = generic1
        self.generic2 = generic2

class _RootWithIdenticalGenericDependencies:
    def __init__(
        self,
        generic1: _IGeneric[_GenericTypeArg1],
        generic2: _IGeneric[_GenericTypeArg1]
    ) -> None:
        self.generic1 = generic1
        self.generic2 = generic2

class _RootWithListOfGenericDependencies:
    def __init__(
        self,
        generics: tuple[_IGeneric[_GenericTypeArg1], ...]
    ) -> None:
        self.generics = list(generics)

class _NullResolver(IResolver):
    def resolve(
        self,
        context: ResolverContext,
        registration: InjectableRegistration,
        injectable_type: type
    ) -> Any:
        return None

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
        of a singleton as the parent lifetime scope.
        """

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

    def test_resolve_should_return_the_correct_instance_for_instance_registration(self):
        """Asserts that the lifetime scope correctly returns the
        already existing instance for a by-instance registration.
        """

        instance = _TestInstanceService()
        catalog = (InjectableCatalogBuilder()
            .register_instance(instance, (_ITestService,))
            .build()
        )
        scope = LifetimeScope(catalog)

        resolved_instance = scope.resolve(_TestInstanceService)

        self.assertIsNotNone(resolved_instance)
        self.assertIs(resolved_instance, instance)

    def test_resolve_should_resolve_instance_dependent_injectable_correctly(self):
        """Asserts that the lifetime scope correctly resolves
        an injectable that depends on another one registered as an instance.
        """

        instance = _TestInstanceService()
        catalog = (InjectableCatalogBuilder()
            .register_instance(instance, (_ITestService,))
            .register_type(_InstanceDependent, (_InstanceDependent,))
            .build()
        )
        scope = LifetimeScope(catalog)

        resolved_instance = scope.resolve(_InstanceDependent)

        self.assertIsNotNone(resolved_instance)
        self.assertIsNotNone(resolved_instance.test_service)
        self.assertIs(resolved_instance.test_service, instance)

    def test_resolve_should_raise_when_no_resolver_can_resolve_a_dependency(self):
        """Asserts that the lifetime scope raises an exception
        when none of the available resolvers can resolve
        an instance of the injectable.
        """

        catalog = (InjectableCatalogBuilder()
            .register_type(Transient1, (Transient1,))
            .build()
        )
        scope = LifetimeScope(catalog, (_NullResolver(),))

        self.assertRaises(
            DependencyResolutionException,
            lambda: scope.resolve(Transient1)
        )

    def test_resolve_should_resolve_correctly_for_generic_type(self):
        """Asserts that the lifetime scope correctly resolves
        injectables registered in a generic fashion.
        """

        catalog = (InjectableCatalogBuilder()
            .register_type(_RootWithDifferentGenericDependencies, (_RootWithDifferentGenericDependencies,))
            .register_type(_TestInstanceService, (_ITestService,), InjectableScopeType.SINGLETON)
            .register_generic(_GenericImpl, (_IGeneric,))
            .build()
        )
        scope = LifetimeScope(catalog)

        resolved_instance = scope.resolve(_RootWithDifferentGenericDependencies)

        self.assertIsNotNone(resolved_instance)
        self.assertIsNotNone(resolved_instance.generic1)
        self.assertIsNotNone(resolved_instance.generic2)
        self.assertIsNotNone(resolved_instance.generic1.value)
        self.assertIsNotNone(resolved_instance.generic2.value)

    def test_resolve_should_resolve_correctly_for_generic_type_with_identical_singletons(self):
        """Asserts that the lifetime scope correctly resolves
        the same instance registered in a generic fashion.
        """

        catalog = (InjectableCatalogBuilder()
            .register_type(_RootWithIdenticalGenericDependencies, (_RootWithIdenticalGenericDependencies,))
            .register_type(_TestInstanceService, (_ITestService,), InjectableScopeType.SINGLETON)
            .register_generic(_GenericImpl, (_IGeneric,), InjectableScopeType.SINGLETON)
            .build()
        )
        scope = LifetimeScope(catalog)

        resolved_instance = scope.resolve(_RootWithIdenticalGenericDependencies)

        self.assertIsNotNone(resolved_instance)
        self.assertIsNotNone(resolved_instance.generic1)
        self.assertIs(resolved_instance.generic1, resolved_instance.generic2)

    def test_resolve_should_resolve_correctly_for_generic_type_list(self):
        """Asserts that the lifetime scope correctly resolves
        a list of injectables registered in a generic fashion.
        """

        catalog = (InjectableCatalogBuilder()
            .register_type(_RootWithListOfGenericDependencies, (_RootWithListOfGenericDependencies,))
            .register_type(_TestInstanceService, (_ITestService,), InjectableScopeType.SINGLETON)
            .register_generic(_GenericImpl, (_IGeneric,))
            .register_generic(_GenericImpl2, (_IGeneric,))
            .build()
        )
        scope = LifetimeScope(catalog)

        resolved_instance = scope.resolve(_RootWithListOfGenericDependencies)

        self.assertIsNotNone(resolved_instance)
        self.assertIsNotNone(resolved_instance.generics)
        self.assertEqual(len(resolved_instance.generics), 2)
        assert_contains(resolved_instance.generics, lambda i: issubclass(type(i), _GenericImpl))
        assert_contains(resolved_instance.generics, lambda i: issubclass(type(i), _GenericImpl2))
        assert_contains_unique(resolved_instance.generics, type)

    def test_resolve_should_resolve_correctly_when_generic_injectable_is_not_found_for_list_dependency(self):
        """Asserts that the lifetime scope correctly resolved
        the injectable when its list of generic injectables dependency
        cannot be satisfied.
        """

        catalog = (InjectableCatalogBuilder()
            .register_type(_RootWithListOfGenericDependencies, (_RootWithListOfGenericDependencies,))
            .build()
        )
        scope = LifetimeScope(catalog)

        resolved_instance = scope.resolve(_RootWithListOfGenericDependencies)

        self.assertIsNotNone(resolved_instance)
        self.assertIsNotNone(resolved_instance.generics)
        self.assertEqual(len(resolved_instance.generics), 0)

    def test_resolve_should_raise_when_generic_injectable_is_not_found(self):
        """Asserts that the lifetime scope raises an exception
        when the required generic injectable hasn't been registered.
        """

        catalog = (InjectableCatalogBuilder()
            .register_type(_RootWithIdenticalGenericDependencies, (_RootWithIdenticalGenericDependencies,))
            .build()
        )
        scope = LifetimeScope(catalog)

        self.assertRaises(
            DependencyResolutionException,
            lambda: scope.resolve(_RootWithIdenticalGenericDependencies)
        )

if __name__ == "__main__":
    unittest.main()
