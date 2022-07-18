from .protocol_interface import ProtocolInterface
from kanata.decorators import injectable

@injectable(ProtocolInterface)
class ProtocolImpl(ProtocolInterface):
    """A class that implements ProtocolInterface."""
