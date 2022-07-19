from .inon_dependee import INonDependee
from .protocol_interface import ProtocolInterface
from kanata.decorators import injectable

@injectable(INonDependee)
class ProtocolDependent(INonDependee):
    def __init__(self, protocol_impl: ProtocolInterface) -> None:
        self.injected = protocol_impl
