from .isingleton import ISingleton
from .itransient1 import ITransient1
from .itransient2 import ITransient2
from kanata.decorators import injectable, scope
from kanata.models import InjectableScopeType

@scope(InjectableScopeType.SINGLETON)
@injectable(ISingleton)
@injectable(ITransient1)
@injectable(ITransient2)
class Singleton(ITransient1, ITransient2, ISingleton):
    """A singleton dependent type with three contracts for testing."""

    def __init__(self) -> None:
        super().__init__()
