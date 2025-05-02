from typing import Optional

from pyalex import Works
import pyalex

from bibly.base_handler import SearchHandler
from bibly.handler_registry import HandlerRegistry
from bibly.utils import get_field_value, log_count, log_initialization, log_search, SearchResult

class OpenAlexHandler(SearchHandler):
    # No required parameters for OpenAlex
    required_params = []

    @log_initialization
    def initialize(self):
        """ Initialize the OpenAlex search handler with API email."""
        pyalex.config.email = self.email
    
    @log_count
    def count(self,
              query: str,
              year_from: Optional[str | int] = None,
              year_to: Optional[str | int] = None) -> int:
        """ Count the number of results for a given query using the OpenAlex API."""
        count = (Works().search(query)
                        .filter(from_publication_date=f'{year_from}-01-01',
                                to_publication_date=f'{year_to}-12-31')
                        .count())
        return count

    @log_search
    def search(self,
               query: str,
               year_from: Optional[str | int] = None,
               year_to: Optional[str | int] = None) -> list[SearchResult]:
        """ Search for a given query using the OpenAlex API."""
        pager = (Works().search(query)
                .filter(from_publication_date=f'{year_from}-01-01',
                        to_publication_date=f'{year_to}-12-31')
                .paginate(per_page=200))
        
        results = []
        for page in pager:
            for document in page:
                doi = get_field_value(document, 'doi', '').replace('https://doi.org/', '') or None
                
                authorships = get_field_value(document, 'authorships', [])
                authors = '; '.join([a.get('author', {}).get('display_name') for a in authorships])

                results.append(SearchResult(
                    doi=doi,
                    title=document.get('title'),
                    abstract=document.get('abstract'),
                    authors=authors,
                    date=document.get('publication_date'),
                    source='OpenAlex'
                ))
        
        return results


    def __init__(self, **kwargs):
        """
        Handler for OpenAlex API

        :param email: Personal email for OpenAlex API
        """
        self.email = kwargs.get('email')
        super().__init__()
