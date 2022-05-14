from enum import IntEnum

class InjectableScopeType(IntEnum):
    """Defines the valid types of an injectable's lifetime scope."""

    TRANSIENT = 0
    """Marks the injectable as transient,
    meaning a new instance is created for each dependency.
    """

    SINGLETON = 1
    """Marks the injectable as a singleton,
    meaning it persists throughout an entire lifetime scope.
    """
