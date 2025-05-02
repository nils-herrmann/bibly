from typing import Optional

from pybliometrics.sciencedirect import init, ScienceDirectSearch

from bibly.base_handler import SearchHandler
from bibly.handler_registry import HandlerRegistry
from bibly.utils import log_count, log_initialization, log_search, SearchResult

class SciencedirectHandler(SearchHandler):
    required_params = ['scopus_key', 'scopus_token']

    @log_initialization
    def initialize(self):
        """
        Initialize the Scopus search handler with API key and token.

        :param api_key: Scopus API key
        :param api_token: Scopus API token
        """
        if self.api_token:
            init(keys=[self.api_key], inst_tokens=[self.api_token])
        else:
            init(keys=[self.api_key])

    @log_count
    def count(self,
              query: str,
              year_from: Optional[str | int] = None,
              year_to: Optional[str | int] = None) -> int:
        """ Count the number of results for a given query using the ScienceDirectSearch API."""
        return 0

    @log_search
    def search(self,
               query: str,
               year_from: Optional[str | int] = None,
               year_to: Optional[str | int] = None) -> list[SearchResult]:
        """ Search for a given query using the ScienceDirectSearch API."""
        query += f" AND DATE({year_from}-{year_to})" if year_from or year_to else ""

        sciencedirect_search = ScienceDirectSearch(query)

        results = []
        if sciencedirect_search.results:
            for entry in sciencedirect_search.results:
                results.append(
                    SearchResult(
                        doi=entry.doi,
                        title=entry.title,
                        abstract=None,
                        authors=entry.authors,
                        date=entry.coverDate,
                        source="ScienceDirect"
                    )
                )
        return results


    def __init__(self, **kwargs):
        """
        Initialize the ScienceDirect search handler with API key and token.

        :param api_key: ScienceDirect API key
        :param api_token: ScienceDirect API token
        """
        self.api_key = kwargs.get('scopus_key')
        self.api_token = kwargs.get('scopus_token')
        super().__init__()

