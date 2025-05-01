from typing import Optional

from pybliometrics.scopus import init, ScopusSearch

from bibly.search_handler import SearchHandler
from bibly.utils import log_count, log_search, SearchResult


class ScopusHandler(SearchHandler):
    def initialize(self):
        """ 
        Initialize the Scopus search handler with API key and token.
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
        """ Count the number of results for a given query using the Scopus API."""
        query += f" AND PUBYEAR > {year_from - 1}" if year_from else ""
        query += f" AND PUBYEAR < {year_to + 1}" if year_to else ""

        scopus_search = ScopusSearch(query, download=False, refresh=True)
        return scopus_search.get_results_size()
        
    
    @log_search
    def search(self,
               query: str,
               year_from: Optional[str | int] = None,
               year_to: Optional[str | int] = None) -> list[SearchResult]:
        """ Search for a given query using the Scopus API."""
        query += f" AND PUBYEAR > {year_from - 1}" if year_from else ""
        query += f" AND PUBYEAR < {year_to + 1}" if year_to else ""

        scopus_search = ScopusSearch(query)

        results = []
        if scopus_search.results:
            for entry in scopus_search.results:
                results.append(
                    SearchResult(
                        doi=entry.doi,
                        title=entry.title,
                        abstract=entry.description,
                        authors=entry.author_names,
                        date=entry.coverDate,
                        source="Scopus"
                    )
                )
        return results


    def __init__(self,
                 api_key: str,
                 api_token: Optional[str]):
        """
        Initialize the Scopus search handler with API key and token.

        :param api_key: Scopus API key
        :param api_token: Scopus API token
        """
        self.api_key = api_key
        self.api_token = api_token
        self.initialize()
