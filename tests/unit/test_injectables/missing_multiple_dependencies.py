from .inon_dependee import INonDependee
from .iunused import IUnused
from kanata.decorators import injectable
from typing import Tuple

@injectable(INonDependee)
class MissingMultipleDependencies(INonDependee):
    """An injectable with a multi-dependency that has no implementation for testing."""

    def __init__(self, unuseds: Tuple[IUnused, ...]) -> None: # pylint: disable=unused-argument
        super().__init__()
