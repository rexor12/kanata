from .inon_dependee import INonDependee
from .iscoped import IScoped
from kanata.decorators import injectable, scope
from kanata.models import InjectableScopeType

@scope(InjectableScopeType.SINGLETON)
@injectable(INonDependee)
class CaptiveScopedDependency(INonDependee):
    """A singleton dependent type that depends on a scoped instance."""

    def __init__(self, scoped: IScoped) -> None: # pylint: disable=unused-argument
        super().__init__()
