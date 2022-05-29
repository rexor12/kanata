from .iscoped import IScoped
from kanata.decorators import injectable, scope
from kanata.models import InjectableScopeType

@scope(InjectableScopeType.SCOPED)
@injectable(IScoped)
class Scoped(IScoped):
    """A scoped injectable for testing."""
