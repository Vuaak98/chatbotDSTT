#!/usr/bin/env python3
"""
Qdrant smoke check (safe, read-only):
- Load .env
- Connect to Qdrant Cloud
- Inspect collection + named vectors
- Count points
- Run two light searches:
  1) Pure semantic
  2) Semantic over a full-text filtered subset (if supported)
- Fuse with RRF and print sample payload fields

Notes:
- Does NOT modify or delete anything
- Uses only the collection name from .env
- Requires: qdrant-client, python-dotenv, openai (for embeddings)
"""
import os
import time
from typing import List, Tuple, Dict, Any

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import OpenAI


def load_env():
    load_dotenv()
    cfg = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "QDRANT_URL": os.getenv("QDRANT_URL"),
        "QDRANT_API_KEY": os.getenv("QDRANT_API_KEY"),
        "QDRANT_COLLECTION_NAME": os.getenv("QDRANT_COLLECTION_NAME", "math_collection"),
        "EMBEDDING_MODEL": os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
    }
    missing = [k for k, v in cfg.items() if not v and k != "EMBEDDING_MODEL"]
    if missing:
        raise RuntimeError(f"Missing env vars: {missing}")
    return cfg


def rrf_fuse(list_a, list_b, k: int = 60, top_k: int = 10):
    """Reciprocal Rank Fusion for two result lists from Qdrant.
    Each item must have an 'id' attribute.
    """
    ranks: Dict[Any, float] = {}
    for rank, p in enumerate(list_a, start=1):
        ranks[p.id] = ranks.get(p.id, 0.0) + 1.0 / (k + rank)
    for rank, p in enumerate(list_b, start=1):
        ranks[p.id] = ranks.get(p.id, 0.0) + 1.0 / (k + rank)

    # Keep a map from id to point for payload display
    id_to_point = {}
    for p in list_a:
        if p.id not in id_to_point:
            id_to_point[p.id] = p
    for p in list_b:
        if p.id not in id_to_point:
            id_to_point[p.id] = p

    fused = sorted(ranks.items(), key=lambda x: x[1], reverse=True)
    fused_ids = [pid for pid, _ in fused[:top_k]]
    return [id_to_point[pid] for pid in fused_ids if pid in id_to_point]


def make_semantic_vector(openai_client: OpenAI, model: str, text: str) -> List[float]:
    resp = openai_client.embeddings.create(model=model, input=text)
    return resp.data[0].embedding


def try_full_text_filter(query: str):
    """Build a Qdrant full-text filter against natural_language_desc and latex_string if supported.
    Returns a models.Filter or None if not applicable.
    """
    must = []
    try:
        must.append(
            models.FieldCondition(
                key="natural_language_desc",
                match=models.MatchText(text=query),
            )
        )
        # Optionally include latex_string too (comment in if desired)
        # must.append(
        #     models.FieldCondition(
        #         key="latex_string",
        #         match=models.MatchText(text=query),
        #     )
        # )
        return models.Filter(must=must)
    except Exception:
        # Older Qdrant deployments may not support MatchText via client
        return None


def main():
    cfg = load_env()

    # Init clients
    openai_client = OpenAI(api_key=cfg["OPENAI_API_KEY"])  # Do not print the key
    qdrant = QdrantClient(url=cfg["QDRANT_URL"], api_key=cfg["QDRANT_API_KEY"])

    collection = cfg["QDRANT_COLLECTION_NAME"]
    print(f"[INFO] Qdrant URL: {cfg['QDRANT_URL']}")
    print(f"[INFO] Collection: {collection}")

    # Inspect collection info
    info = qdrant.get_collection(collection_name=collection)
    print("\n[INFO] Collection info:")
    try:
        # For named vectors
        vectors_cfg = info.config.params.vectors
        if isinstance(vectors_cfg, dict):
            print("  Named vectors:")
            for name, vp in vectors_cfg.items():
                print(f"     - {name}: size={vp.size}, distance={vp.distance}")
        else:
            print(f"  Single unnamed vector: size={vectors_cfg.size}, distance={vectors_cfg.distance}")
    except Exception:
        print("  WARNING: Unable to read vector config details (client/version mismatch)")

    # Count points
    try:
        count = qdrant.count(collection_name=collection, exact=False).count
        print(f"  Estimated points: {count}")
    except Exception as e:
        print(f"  WARNING: Count failed: {e}")

    # Build example query
    sample_query = os.getenv("QDRANT_SMOKE_QUERY", "bài tập ma trận năm 2024")
    print(f"\n[QUERY] Sample query: {sample_query}")

    # Make semantic vector
    try:
        t0 = time.time()
        sem_vec = make_semantic_vector(openai_client, cfg["EMBEDDING_MODEL"], sample_query)
        t1 = time.time()
        print(f"  OK Embedding created in {t1 - t0:.2f}s")
    except Exception as e:
        print(f"  ERROR Embedding error: {e}")
        return

    # Semantic search (global)
    try:
        sem_results = qdrant.search(
            collection_name=collection,
            query_vector=("semantic_vector", sem_vec),  # named vector expected
            limit=10,
            with_vectors=False,
        )
        print(f"  OK Semantic results: {len(sem_results)}")
    except Exception as e:
        print(f"  ERROR Semantic search error: {e}")
        sem_results = []

    # Full-text subset + semantic re-search (if supported)
    ft_results = []
    ft_filter = try_full_text_filter(sample_query)
    if ft_filter is not None:
        try:
            ft_results = qdrant.search(
                collection_name=collection,
                query_vector=("semantic_vector", sem_vec),
                query_filter=ft_filter,
                limit=10,
                with_vectors=False,
            )
            print(f"  OK FT-subset semantic results: {len(ft_results)}")
        except Exception as e:
            print(f"  WARNING FT-subset search failed (continuing): {e}")
    else:
        print("  WARNING: Full-text filter not supported by client/deployment; skipping FT-subset search")

    # RRF fusion
    fused = rrf_fuse(sem_results, ft_results, k=60, top_k=5)

    # Print sample
    def safe_get(d, *keys):
        cur = d
        for k in keys:
            if not isinstance(cur, dict) or k not in cur:
                return None
            cur = cur[k]
        return cur

    print("\n[RESULTS] Top fused results (up to 5):")
    for i, p in enumerate(fused, start=1):
        payload = p.payload or {}
        title = payload.get("title")
        cat = payload.get("category")
        sub = payload.get("subcategory")
        year = safe_get(payload, "metadata", "year")
        print(f"  {i}. id={p.id} | score={getattr(p, 'score', None)} | {cat}/{sub} | year={year}")
        if title:
            print(f"     title: {title[:120]}")
        # Sanity: required fields
        missing = [k for k in ["doc_id", "source_file", "problem_statement_natural"] if k not in payload]
        if missing:
            print(f"     WARNING: Missing payload fields: {missing}")

    print("\nOK Smoke check done. If results look sane, backend RAG can proceed.")


if __name__ == "__main__":
    main()

