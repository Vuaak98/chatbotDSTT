#!/usr/bin/env python3
"""
Manual smoke test for backend RAG (semantic-only path).
- Loads backend/.env
- Instantiates RAGService and runs get_context for a sample query
- Prints top results with key payload fields

Usage:
  python backend/app/rag/manual_smoke_test.py "bài tập ma trận năm 2024"
"""
import os
import sys
import asyncio
from typing import List
from dotenv import load_dotenv

# Ensure env is loaded from backend/.env
HERE = os.path.dirname(__file__)
BACKEND_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_ROOT, ".."))
ENV_PATH = os.path.join(BACKEND_ROOT, ".env")
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)

# Ensure project root on sys.path so 'backend' package is importable
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Late imports after env and sys.path
from backend.app.rag.rag_service import RAGService  # noqa: E402


async def main():
    default_query = "bài tập ma trận năm 2024"
    args = sys.argv[1:]
    show_full = False
    # Simple flag parsing: support --full to print assembled context (full problem+solution)
    if "--full" in args:
        args.remove("--full")
        show_full = True
    query = " ".join(args) if args else default_query

    print(f"[INFO] Using .env at: {ENV_PATH if os.path.exists(ENV_PATH) else 'not found'}")
    print(f"[QUERY] {query}")

    rag = RAGService()
    docs, ok = await rag.get_context(query=query, k=5, use_query_metadata=False)
    print(f"[INFO] Retrieval success: {ok}, results: {len(docs)}")

    def md_get(md: dict, *keys, default=None):
        cur = md
        for k in keys:
            if not isinstance(cur, dict) or k not in cur:
                return default
            cur = cur[k]
        return cur

    for i, d in enumerate(docs[:5], start=1):
        md = getattr(d, "metadata", {}) or {}
        title = md.get("title")
        cat = md.get("category")
        sub = md.get("subcategory")
        year = md_get(md, "metadata", "year")
        print(f"  {i}. {title!s} | {cat}/{sub} | year={year}")
        preview = getattr(d, "page_content", "")[:140].replace("\n", " ")
        print(f"     content: {preview}")

    if not docs:
        print("[WARN] No documents returned. Check Qdrant_URL, Collection, API key, or embeddings.")
        return

    # Optionally print full assembled context (problem + solution) using the same logic as chat flow
    if show_full:
        print("\n[FULL CONTEXT]")
        context = rag.format_context_for_prompt(docs)
        print(context)


if __name__ == "__main__":
    asyncio.run(main())

