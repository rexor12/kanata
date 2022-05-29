from .inon_dependee import INonDependee
from .itransient1 import ITransient1
from kanata.decorators import injectable, scope
from kanata.models import InjectableScopeType

@scope(InjectableScopeType.SINGLETON)
@injectable(INonDependee)
class CaptiveTransientDependency(INonDependee):
    """A singleton dependent type that depends on a transient instance."""

    def __init__(self, transient: ITransient1) -> None: # pylint: disable=unused-argument
        super().__init__()
