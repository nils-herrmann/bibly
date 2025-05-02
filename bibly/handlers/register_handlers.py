from bibly.handlers.sciencedirect_handler import SciencedirectHandler
from bibly.handlers.scopus_handler import ScopusHandler
from bibly.handlers.springer_handler import SpringerHandler
from bibly.handlers.openalex_handler import OpenAlexHandler

# Import the HandlerRegistry to ensure handlers are registered
from bibly.handler_registry import HandlerRegistry

# Explicitly register all handlers
HandlerRegistry.register_handler("ScienceDirect", SciencedirectHandler)
HandlerRegistry.register_handler("Scopus", ScopusHandler)
HandlerRegistry.register_handler("Springer", SpringerHandler)
HandlerRegistry.register_handler("OpenAlex", OpenAlexHandler)