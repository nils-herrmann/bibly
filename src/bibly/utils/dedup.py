import re

from bibly.utils.data_types import SearchResult

_WHITESPACE_RE = re.compile(r"\s+")


def _normalize_title(title: str | None) -> str | None:
    """Lower-case, strip, and collapse internal whitespace. Empty titles map to None."""
    if not title:
        return None
    normalized = _WHITESPACE_RE.sub(" ", title.strip().lower())
    return normalized or None


def _normalize_doi(doi: str | None) -> str | None:
    """Lower-case and strip the DOI. Empty DOIs map to None."""
    if not doi:
        return None
    normalized = doi.strip().lower()
    return normalized or None


def deduplicate(results: list[SearchResult]) -> list[SearchResult]:
    """
    Remove duplicate search results, keeping the first occurrence.

    Two entries are considered duplicates if they share the same normalized
    title OR the same DOI. Empty titles and empty DOIs never match, so entries
    lacking both are always kept.

    :param results: The search results to deduplicate.

    :return: The deduplicated results, in their original order.
    """
    seen_titles: set[str] = set()
    seen_dois: set[str] = set()
    unique: list[SearchResult] = []

    for result in results:
        title_key = _normalize_title(result.title)
        doi_key = _normalize_doi(result.doi)

        is_duplicate = (title_key is not None and title_key in seen_titles) or \
                       (doi_key is not None and doi_key in seen_dois)
        if is_duplicate:
            continue

        if title_key is not None:
            seen_titles.add(title_key)
        if doi_key is not None:
            seen_dois.add(doi_key)
        unique.append(result)

    return unique
