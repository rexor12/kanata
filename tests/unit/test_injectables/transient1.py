from .itransient1 import ITransient1
from kanata.decorators import injectable

@injectable(ITransient1)
class Transient1(ITransient1):
    """A dependent type for testing."""

    def __init__(self) -> None:
        super().__init__()
