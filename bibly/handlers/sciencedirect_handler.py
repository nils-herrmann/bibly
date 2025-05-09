from typing import Optional

from pybliometrics.sciencedirect import init, ArticleMetadata, ScienceDirectSearch

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
        q = {'qs': query, 'date': f'{year_from}-{year_to}', 'display': {'show': 1}}
        sciencedirect_results = ScienceDirectSearch(q, download=False, refresh=True)

        return sciencedirect_results.get_results_size()

    @log_search
    def search(self,
               query: str,
               year_from: Optional[str | int] = None,
               year_to: Optional[str | int] = None) -> list[SearchResult]:
        """ Search for a given query using the ScienceDirectSearch API."""
        # Search for dois using the ScienceDirectSearch API
        q = {'qs': query, 'date': f'{year_from}-{year_to}'}
        search_results = ScienceDirectSearch(q)

        results = []
        if search_results.results:
            # Get all metadata including the asbtract
            dois = [d.doi for d in search_results.results]
            q = ' OR '.join([f'DOI({doi})' for doi in dois])
            metadata_results = ArticleMetadata(q)

            for entry in metadata_results.results:
                results.append(
                    SearchResult(
                        doi=entry.doi,
                        title=entry.title,
                        abstract=entry.abstract_text,
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

