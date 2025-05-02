from typing import Optional
from sprynger import init, Meta

from bibly.base_handler import SearchHandler
from bibly.handler_registry import HandlerRegistry
from bibly.utils import log_count, log_search, SearchResult


class SpringerHandler(SearchHandler):
    required_params = ['springer_key']

    def initialize(self):
        """
        Initialize the Springer search handler with API key.
        """
        init(api_key = self.api_key)

    @log_count
    def count(self,
              query: str,
              year_from: Optional[str | int] = None,
              year_to: Optional[str | int] = None) -> int:
          """ Count the number of results for a given query using the Springer API."""
          query += f" AND datefrom:{year_from}-01-01" if year_from else ""
          query += f" AND dateto:{year_to}-12-31" if year_to else ""
    
          springer_search = Meta(query, nr_results=1, refresh=True)
          return springer_search.results.total

    @log_search
    def search(self,
               query: str,
               year_from: Optional[str | int] = None,
               year_to: Optional[str | int] = None) -> list[SearchResult]:
        """ Search for a given query using the Springer API."""
        query += f" AND datefrom:{year_from}-01-01" if year_from else ""
        query += f" AND dateto:{year_to}-12-31" if year_to else ""

        springer_search = Meta(query, nr_results=500)

        results = []
        for entry in springer_search:
            creators = '; '.join([c.creator for c in entry.creators])
            results.append(
                SearchResult(
                    doi=entry.doi,
                    title=entry.title,
                    abstract=entry.abstract,
                    authors=creators,
                    date=entry.publicationDate,
                    source="Springer"
                )
            )
        return results

    def __init__(self, **kwargs):
        """
        Initialize the Springer search handler with API key.

        :param springer_key: Springer API key
        """
        self.api_key = kwargs.get('springer_key')
        super().__init__()
