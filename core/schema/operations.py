"""VCP Protocol Operations"""

from dataclasses import dataclass
from typing import Any


@dataclass
class Document:
    id: str
    text: str
    metadata: dict[str, Any] | None = None


@dataclass
class SearchQuery:
    query: str
    limit: int = 10
    metadata_filters: dict[str, Any] | None = None


@dataclass
class SearchResult:
    id: str
    text: str
    score: float
    metadata: dict[str, Any] | None = None
