from abc import ABCMeta, abstractmethod

class ICalculator(metaclass=ABCMeta):
    """Interface for a calculator."""

    @abstractmethod
    def calculate(self, operation_code: str, value1: float, value2: float) -> float:
        """Calculates the result of the given values
        for the operation specified by the given code.

        :param operation_code: The code of the operation to execute.
        :type operation_code: str
        :param value1: The first value.
        :type value1: float
        :param value2: The second value.
        :type value2: float
        :raises ValueError: Raised when the specified operation is invalid.
        :return: The result of the operation.
        :rtype: float
        """
