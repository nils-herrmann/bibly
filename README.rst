BibLy
=====
`BibLy` is a Python library designed to streamline academic literature searches by integrating multiple APIs (e.g., Scopus, Springer, ScienceDirect, OpenAlex). It provides a unified interface for querying, filtering, and retrieving research articles, enabling efficient data collection and analysis for literature reviews.

🔨 Implemented APIs
-------------------

.. list-table::
   :header-rows: 1

   * - API Name
     - Implemented
   * - Scopus
     - ✅
   * - Springer
     - ✅
   * - ScienceDirect
     - ✅
   * - OpenAlex
     - ✅
   * - Web of Science
     - ❌


⬇️ Install
-----------
Download and install the package from PyPI:

.. code-block:: bash

    pip install bibly


🔑 API Keys
-----------
Each API requires its own credentials. Provide the keys for the APIs you want to
query; handlers without valid credentials are simply skipped.

.. list-table::
   :header-rows: 1

   * - API
     - Parameter
     - Where to get it
     - Cost
   * - OpenAlex
     - ``openalex_key``
     - https://openalex.org/settings/api-key
     - Free
   * - Scopus
     - ``scopus_key``
     - https://dev.elsevier.com/apikey/manage
     - ⚠️ Not free — requires an Elsevier/Scopus subscription (typically institutional).
   * - Springer
     - ``springer_key``
     - https://dev.springernature.com
     - Free


🪧 Example Use
---------------

.. code:: python

    >>> from bibly import BibLy
    >>> # Create client
    >>> client = BibLy(openalex_key="API key for OpenAlex: https://openalex.org/settings/api-key",
    >>>                scopus_key="API key for Scopus: https://dev.elsevier.com/apikey/manage",
    >>>                springer_key="API key for Springer: https://dev.springernature.com",)
    >>> # Count the number of results
    >>> count = client.count(query="iab-bamf-soep AND integration", year_from=2015, year_to=2017)
    >>> count
    {'OpenAlex': 196, 'Scopus': 243, 'Springer': 199}
    >>> # Search using two keywords
    >>> results = client.search(query="iab-bamf-soep AND integration", year_from=2015, year_to=2017)
    >>> results
    [SearchResult(doi='10.13094/smi...', title='Sampling in ...', abstract=None, authors='Simon Kühne; Jannes Jacobsen...', date='2019-04-02', source='OpenAlex'),
     ...]
