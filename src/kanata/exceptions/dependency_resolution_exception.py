from typing import Any

class DependencyResolutionException(Exception):
    """Raised when dependency resolution fails."""

    def __init__(
        self,
        related_type: type[Any] | None = None,
        message: str | None = None) -> None:
        """Initializes a new instance.

        :param related_type: An optional type related to the exception, defaults to None.
        :type related_type: type[Any], optional
        :param message: An optional message that describes the problem, defaults to None.
        :type message: str, optional
        """

        super().__init__(message)
        self.__related_type: type[Any] | None = related_type

    @property
    def related_type(self) -> type[Any] | None:
        """Gets the type related to the exception.

        :return: The type related to the exception.
        :rtype: type[Any] | None
        """

        return self.__related_type
