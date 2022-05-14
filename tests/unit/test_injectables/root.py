from .itransient1 import ITransient1
from .itransient2 import ITransient2
from .iroot import IRoot
from kanata.decorators import injectable
from typing import Tuple

@injectable(IRoot)
class Root(IRoot):
    """Root injectable for testing."""

    def __init__(self,
                 injectables1: Tuple[ITransient1, ...],
                 injectables2: Tuple[ITransient2, ...]) -> None:
        super().__init__()
        self.injectables1: Tuple[ITransient1, ...] = injectables1
        self.injectables2: Tuple[ITransient2, ...] = injectables2
