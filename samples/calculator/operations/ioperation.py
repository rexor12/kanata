from abc import ABCMeta, abstractmethod

class IOperation(metaclass=ABCMeta):
    """Interface for a calculator operation."""

    @property
    @abstractmethod
    def code(self) -> str:
        """Gets the code of the operation.

        :return: The operation code.
        :rtype: str
        """

    @abstractmethod
    def execute(self, *args: float) -> float:
        """Executes the operation and returns the result.

        :return: The result of the operation.
        :rtype: float
        """
