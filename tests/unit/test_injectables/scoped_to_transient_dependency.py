from .inon_dependee import INonDependee
from .itransient1 import ITransient1
from kanata.decorators import injectable, scope
from kanata.models import InjectableScopeType

@scope(InjectableScopeType.SCOPED)
@injectable(INonDependee)
class ScopedToTransientDependency(INonDependee):
    """A scoped dependent type that depends on a transient instance."""

    def __init__(self, transient: ITransient1) -> None: # pylint: disable=unused-argument
        super().__init__()
