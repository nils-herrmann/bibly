from typing import Optional

from bibly.handler_registry import HandlerRegistry
from bibly.handlers import *
from bibly.utils import SearchResult


class BibLy:
    """A class to create a client for BibLy."""
    def count(self,
              query: str,
              year_from: Optional[str | int] = None,
              year_to: Optional[str | int] = None) -> dict[str, int]:
        """
        Count the number of results for a given query for each API.
        """
        counts = {}
        for name, handler in self.handlers.items():
            counts[name] = handler.count(query, year_from, year_to)
        return counts

    def search(self,
               query: str,
               year_from: Optional[str | int] = None,
               year_to: Optional[str | int] = None) -> list[SearchResult]:
        """
        Search for a given query using the initialized search handlers.

        :param query: The search query
        :param year_from: Optional start year for the search
        :param year_to: Optional end year for the search
        
        :return: List of search results
        """
        results = []
        for handler in self.handlers.values():
            results.extend(handler.search(query, year_from, year_to))
        return results

    def __init__(self, **kwargs):
        """
        To use the different APIs, you need to provide the API keys with the exception of
        OpenAlex, which is always available.

        :param email: Personal email for OpenAlex API for the `polite pool <https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication#the-polite-pool>`__.
        :param scopus_key: Scopus API key
        :param scopus_token: Scopus API token
        :param springer_key: Springer API key
        """
        self.handlers = HandlerRegistry.initialize_handlers(**kwargs)
