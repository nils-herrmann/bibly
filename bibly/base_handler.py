from abc import ABC, abstractmethod
from typing import Optional

from bibly.utils import log_count, log_search, SearchResult


class SearchHandler(ABC):
    """Abstract base class for search handlers."""

    # Define required parameters for initialization
    required_params: list[str] = []

    def __init__(self):
        """Ensure the handler is initialized during instantiation."""
        self.initialize()
    
    @classmethod
    def can_initialize(cls, **kwargs) -> bool:
        """
        Check if the handler can be initialized with the given parameters.

        :param kwargs: Parameters to validate
        :return: True if all required parameters are present, False otherwise
        """
        return all(param in kwargs and kwargs[param] is not None for param in cls.required_params)

    @abstractmethod
    def initialize(self):
        """Initialize the search handler."""
        pass

    @abstractmethod
    @log_count
    def count(self,
              query: str,
              year_from: Optional[str | int] = None,
              year_to: Optional[str | int] = None) -> int:
        """Count the number of results for a given query."""
        pass

    @abstractmethod
    @log_search
    def search(self,
               query: str,
               year_from: Optional[str | int] = None,
               year_to: Optional[str | int] = None) -> list[SearchResult]:
        """Search for a given query."""
        pass
