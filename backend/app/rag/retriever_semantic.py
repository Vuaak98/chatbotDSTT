"""
Semantic-only retriever using Qdrant query_points and Vietnamese query parsing.
- Uses named vector 'semantic_vector'
- Applies filters: category, subcategory, metadata.year (if present)
- Returns raw Qdrant points
"""
from __future__ import annotations
from typing import Optional, List, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import OpenAI
import os

from .query_extractor_vn import parse_query, build_qdrant_filter


class SemanticRetriever:
    def __init__(self, qdrant: QdrantClient, openai_client: OpenAI, collection_name: str, embedding_model: str = "text-embedding-3-small"):
        self.qdrant = qdrant
        self.openai = openai_client
        self.collection = collection_name
        self.embedding_model = embedding_model

    def embed(self, text: str):
        resp = self.openai.embeddings.create(model=self.embedding_model, input=text)
        return resp.data[0].embedding

    def retrieve(self, query: str, top_k: int = 10) -> List[Any]:
        parsed = parse_query(query)
        vec = self.embed(parsed.normalized_query)
        qfilter = build_qdrant_filter(parsed.category, parsed.subcategory, parsed.year)

        req = models.QueryRequest(
            query=models.NearestQuery(vector=models.NamedVector(name="semantic_vector", vector=vec)),
            limit=top_k,
            with_payload=True,
            with_vectors=False,
            filter=qfilter,
        )
        res = self.qdrant.query_points(collection_name=self.collection, query=req)
        return list(res.points or [])

