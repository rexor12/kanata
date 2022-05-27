from .ioperation import IOperation
from kanata.decorators import injectable

@injectable(IOperation)
class Add(IOperation):
    """An operation that calculates the result of an addition of two numbers."""

    @property
    def code(self) -> str:
        return "+"

    def execute(self, *args: float) -> float:
        return args[0] + args[1]
