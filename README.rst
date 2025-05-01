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
     - ❌
   * - OpenAlex
     - ✅
   * - Web of Science
     - ❌


⬇️ Install
-----------
Download and install the package from PyPI:

.. code-block:: bash

    pip install bibly


🪧 Example Use
---------------

.. code:: python

    >>> from bibly import BibLy
    >>> # Create client
    >>> client = BibLy(email="Email for OpenAlex polite pool",
    >>>                scopus_key="API key for Scopus: https://dev.elsevier.com/apikey/manage",
    >>>                springer_key="Free API key for Springer: https://dev.springernature.com",)
    >>> # Count the number of results
    >>> count = client.count(query="iab-bamf-soep AND integration", year_from=2015, year_to=2017)
    >>> count
    {'OpenAlex': 196, 'Scopus': 243, 'Springer': 199}
    >>> # Search using two keywords
    >>> results = client.search(query="iab-bamf-soep AND integration", year_from=2015, year_to=2017)
    >>> results
    [SearchResult(doi='10.13094/smi...', title='Sampling in ...', abstract=None, authors='Simon Kühne; Jannes Jacobsen...', date='2019-04-02', source='OpenAlex'),
     ...]
