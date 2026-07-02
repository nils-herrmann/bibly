"""Shared constants for Bibly."""
from pathlib import Path

# Dedicated pybliometrics config for Bibly, kept separate from the user's
# global ``~/.config/pybliometrics.cfg`` (which may contain classes/sections
# that are not implemented in the pybliometrics fork Bibly depends on).
# If the file does not exist, pybliometrics creates a fork-compatible one on
# ``init`` using the provided keys.
PYBLIOMETRICS_CONFIG = Path.home() / '.config' / 'pybliometrics_bibly.cfg'
