from typing import Optional

from pybliometrics.sciencedirect import init, ArticleMetadata, ScienceDirectSearch

from bibly.base_handler import SearchHandler
from bibly.utils import log_count, log_initialization, log_search, PYBLIOMETRICS_CONFIG, SearchResult

class SciencedirectHandler(SearchHandler):
    required_params = ['scopus_key']

    # Max number of DOIs per Article Metadata query to avoid overly long requests
    _METADATA_BATCH_SIZE = 25

    @log_initialization
    def initialize(self):
        """
        Initialize the Scopus search handler with API key and token.

        :param api_key: Scopus API key
        :param api_token: Scopus API token
        """
        if self.api_token:
            init(config_path=PYBLIOMETRICS_CONFIG, keys=[self.api_key], inst_tokens=[self.api_token])
        else:
            init(config_path=PYBLIOMETRICS_CONFIG, keys=[self.api_key])

    @log_count
    def count(self,
              query: str,
              year_from: Optional[str | int] = None,
              year_to: Optional[str | int] = None) -> int:
        """ Count the number of results for a given query using the ScienceDirectSearch API."""
        sciencedirect_results = ScienceDirectSearch(query, date=f'{year_from}-{year_to}',
                                                    download=False, refresh=True)

        return sciencedirect_results.get_results_size()

    @log_search
    def search(self,
               query: str,
               year_from: Optional[str | int] = None,
               year_to: Optional[str | int] = None) -> list[SearchResult]:
        """ Search for a given query using the ScienceDirectSearch API."""
        # Search for dois using the ScienceDirectSearch API
        search_results = ScienceDirectSearch(query, date=f'{year_from}-{year_to}')

        results = []
        if search_results.results:
            # Get all metadata including the abstract. The Article Metadata API
            # rejects overly long queries, so batch the DOIs into chunks.
            dois = [d.doi for d in search_results.results if d.doi]
            for i in range(0, len(dois), self._METADATA_BATCH_SIZE):
                batch = dois[i:i + self._METADATA_BATCH_SIZE]
                q = ' OR '.join([f'DOI({doi})' for doi in batch])
                metadata_results = ArticleMetadata(q)

                for entry in metadata_results.results or []:
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

