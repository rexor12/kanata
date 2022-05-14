from .inon_dependee import INonDependee
from .iunused import IUnused
from kanata.decorators import injectable

@injectable(INonDependee)
class MissingSingleDependency(INonDependee):
    """An injectable with a single dependency that has no implementation for testing."""

    def __init__(self, unused: IUnused) -> None: # pylint: disable=unused-argument
        super().__init__()
