from .itransient2 import ITransient2
from kanata.decorators import injectable

@injectable(ITransient2)
class Transient2(ITransient2):
    """A dependent type for testing."""

    def __init__(self) -> None:
        super().__init__()
