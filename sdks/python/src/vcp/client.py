"""VCP Client - Agnóstico e independente"""

from vcp.adapters.base import BaseAdapter


class VCPClient:
    """Client VCP que gerencia adapters"""

    def __init__(self, adapter: BaseAdapter):
        self.adapter = adapter

    async def ingest(self, documents: list[dict]) -> dict:
        return await self.adapter.ingest(documents)

    async def search(self, query: str, limit: int = 10) -> list[dict]:
        return await self.adapter.search(query, limit)

    async def rerank(self, query: str, candidates: list[dict]) -> list[dict]:
        return await self.adapter.rerank(query, candidates)

    async def forget(self, doc_ids: list[str]) -> dict:
        return await self.adapter.forget(doc_ids)
