"""
Context assembly for RAG (semantic-only baseline).
- Consumes Qdrant points (payload dicts) or LangChain Documents
- Builds a Vietnamese context with citations (title/source_file/year)
- Applies a simple character-based budget (approx tokens)
"""
from __future__ import annotations
from typing import List, Dict, Any, Tuple, Optional, Union


def _get_payload(item: Any) -> Dict[str, Any]:
    # Supports Qdrant PointStruct (has .payload) or LangChain Document
    if hasattr(item, "payload") and isinstance(getattr(item, "payload"), dict):
        return item.payload  # Qdrant point
    if hasattr(item, "metadata") and isinstance(getattr(item, "metadata"), dict):
        md = item.metadata.copy()
        # Try to backfill page_content into a natural field if present
        if hasattr(item, "page_content") and item.page_content and "problem_statement_natural" not in md:
            md["problem_statement_natural"] = item.page_content
        return md
    if isinstance(item, dict):
        return item
    return {}


def _estimate_tokens(text: str) -> int:
    # Simple heuristic ~4 chars per token
    return max(1, len(text) // 4)


def _truncate_to_tokens(text: str, max_tokens: int) -> str:
    """Truncate text to approximately max_tokens (heuristic) and add ellipsis if truncated."""
    if not text or max_tokens <= 0:
        return ""
    approx_chars = max_tokens * 4
    if len(text) <= approx_chars:
        return text
    # Reserve a few chars for ellipsis
    cut = max(0, approx_chars - 3)
    return (text[:cut].rstrip()) + "..."


def assemble_context(points: List[Any], budget_tokens: int = 1200) -> Tuple[str, List[Dict[str, Any]]]:
    """Build context string and return also the used payloads for transparency.
    Returns (context_str, used_payloads)

    Policy: Include full problem and full solution by default. If the token budget
    would be exceeded, we prioritize keeping the full problem, and truncate the
    solution to fit. Only if even the problem alone exceeds budget, we truncate
    the problem as a last resort.
    """
    remaining = max(100, budget_tokens)
    lines: List[str] = []
    used_payloads: List[Dict[str, Any]] = []

    for p in points:
        payload = _get_payload(p)
        if not payload:
            continue

        title = payload.get("title")
        source_file = payload.get("source_file")
        year = payload.get("year")  # Schema mới: year ở top level
        category = payload.get("category")
        subcategory = payload.get("subcategory")
        question_number = payload.get("question_number")

        # Compose citation với schema mới
        cite = []
        if title:
            cite.append(str(title))
        if category and subcategory:
            cite.append(f"{category}/{subcategory}")
        elif category:
            cite.append(category)
        if question_number:
            cite.append(f"#{question_number}")
        if year is not None:
            cite.append(f"year={year}")
        header = " | ".join(cite)

        # Build problem text (prefer natural fields, fallback to raw)
        problem_chunks: List[str] = []
        psn = payload.get("problem_statement_natural") or payload.get("problem_statement")
        if psn:
            problem_chunks.append(f"De bai: {psn}")

        ppn = payload.get("problem_parts_natural") or payload.get("problem_parts")
        if isinstance(ppn, dict):
            # Keep stable ordering by key when possible
            for k in sorted(ppn.keys()):
                v = ppn.get(k)
                if v:
                    problem_chunks.append(f"({k}) {v}")

        problem_text = "\n".join(problem_chunks).strip()

        # Build solution text (prefer natural, fallback to raw)
        solution_chunks: List[str] = []
        soln = payload.get("solution_natural")
        raw_soln = payload.get("solution") if not soln else None

        # Full solution
        full_sol = None
        if isinstance(soln, dict):
            full_sol = soln.get("full_solution")
        if full_sol is None and isinstance(raw_soln, dict):
            full_sol = raw_soln.get("full_solution")
        if full_sol:
            solution_chunks.append(f"Loi giai: {full_sol}")

        # Solution parts
        sol_parts = None
        if isinstance(soln, dict):
            sol_parts = soln.get("solution_parts")
        if sol_parts is None and isinstance(raw_soln, dict):
            sol_parts = raw_soln.get("solution_parts")
        if isinstance(sol_parts, dict):
            for k in sorted(sol_parts.keys()):
                v = sol_parts.get(k)
                if v:
                    solution_chunks.append(f"({k}) {v}")

        solution_text = "\n".join(solution_chunks).strip()

        # Skip if no content at all
        if not problem_text and not solution_text:
            continue

        # Compute header cost
        header_cost = _estimate_tokens(header) if header else 0

        # Always try to include header (if any)
        piece_lines: List[str] = []
        if header:
            piece_lines.append(f"### {header}")

        # Attempt to include full problem first
        problem_cost = _estimate_tokens(problem_text) if problem_text else 0
        available = max(0, remaining - header_cost)

        if problem_text:
            if problem_cost <= available:
                piece_lines.append(problem_text)
                available -= problem_cost
            else:
                # Truncate problem as last resort
                truncated = _truncate_to_tokens(problem_text, available)
                if truncated:
                    piece_lines.append(truncated)
                    available = 0
                else:
                    # No room even for truncated problem; stop adding more docs
                    break

        # Then include solution, truncate only if needed
        if solution_text and available > 0:
            sol_cost = _estimate_tokens(solution_text)
            if sol_cost <= available:
                piece_lines.append("")
                piece_lines.append(solution_text)
                available -= sol_cost
            else:
                truncated_sol = _truncate_to_tokens(solution_text, available)
                if truncated_sol:
                    piece_lines.append("")
                    piece_lines.append(truncated_sol)
                    available = 0

        # Finalize this piece
        if piece_lines:
            lines.extend(piece_lines)
            lines.append("")
            used_payloads.append(payload)
            # Update remaining after we used header + (problem/solution) tokens
            used_cost = header_cost + (problem_cost if problem_cost <= (remaining - header_cost) else _estimate_tokens(piece_lines[-1]))
            # Conservative: recompute remaining using text we actually appended
            appended_text = "\n".join(piece_lines)
            remaining -= _estimate_tokens(appended_text)

        if remaining <= 0:
            break

    context = "\n".join(lines).strip()
    return context, used_payloads

