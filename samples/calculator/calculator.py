from .icalculator import ICalculator
from .operations import IOperation
from kanata.decorators import injectable
from typing import Dict, Tuple

@injectable(ICalculator)
class Calculator(ICalculator):
    """Default implementation of a calculator."""

    # The tuple of IOperation implementations will be injected automatically here
    # when an instance of the Calculator type is resolved.
    def __init__(self, operations: Tuple[IOperation, ...]) -> None:
        self.__operations: Dict[str, IOperation] = {
            operation.code: operation for operation in operations
        }

    # Select the appropriate operation and execute it with the parameters.
    def calculate(self, operation_code: str, value1: float, value2: float) -> float:
        if (operation := self.__operations.get(operation_code, None)) is None:
            raise ValueError(f"No operation with code '{operation_code}' was found.")
        return operation.execute(value1, value2)
