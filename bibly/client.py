from typing import Optional

from bibly.openalex_handler import OpenAlexHandler
from bibly.scopus_handler import ScopusHandler
from bibly.sciencedirect_handler import SciencedirectHandler
from bibly.springer_handler import SpringerHandler
from bibly.utils.data_types import SearchResult


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
        counts['OpenAlex'] = self.openalex_handler.count(query, year_from, year_to)
        if self.scopus_handler:
            counts['Scopus'] = self.scopus_handler.count(query, year_from, year_to)
        if self.springer_handler:
            counts['Springer'] = self.springer_handler.count(query, year_from, year_to)

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

        results.extend(self.openalex_handler.search(query, year_from, year_to))
        if self.sciencedirect_handler:
            results.extend(self.sciencedirect_handler.search(query, year_from, year_to))
        if self.scopus_handler:
            results.extend(self.scopus_handler.search(query, year_from, year_to))
        if self.springer_handler:
            results.extend(self.springer_handler.search(query, year_from, year_to))

        return results

    def __init__(self,
                 email: Optional[str] = None,
                 scopus_key: Optional[str] = None,
                 scopus_token: Optional[str] = None,
                 springer_key: Optional[str] = None):
        """
        To use the different APIs, you need to provide the API keys with the exception of
        OpenAlex, which is always available.

        :param email: Personal email for OpenAlex API for the `polite pool <https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication#the-polite-pool>`__.
        :param scopus_key: Scopus API key
        :param scopus_token: Scopus API token
        :param springer_key: Springer API key
        """
        # Initialize API handlers
        self.openalex_handler = OpenAlexHandler(email)
        self.scopus_handler = ScopusHandler(scopus_key, scopus_token) if scopus_key else None
        self.sciencedirect_handler = SciencedirectHandler(scopus_key, scopus_token) if scopus_key else None
        self.springer_handler = SpringerHandler(springer_key) if springer_key else None
