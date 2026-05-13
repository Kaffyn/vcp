"""Base adapter interface"""

from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    """Interface base for all VCP adapters"""

    @abstractmethod
    async def ingest(self, documents: list[dict]) -> dict:
        """Ingest documents into the vector store"""
        pass

    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> list[dict]:
        """Search for documents matching the query"""
        pass

    @abstractmethod
    async def rerank(self, query: str, candidates: list[dict]) -> list[dict]:
        """Rerank documents by relevance"""
        pass

    @abstractmethod
    async def forget(self, doc_ids: list[str]) -> dict:
        """Remove documents from the store"""
        pass
