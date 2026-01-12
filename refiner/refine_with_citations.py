from typing import List, Dict

def refine_context_with_citations(text: str, focus_areas: List[str]) -> List[Dict]:
    """
    Returns a list of kept lines with stable line_ids for citation.
    Output format:
      [{"line_id": 1, "text": "..."}, ...]
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    kept = []
    line_id = 1
    for ln in lines:
        ln_lower = ln.lower()
        if any(key.lower() in ln_lower for key in focus_areas):
            kept.append({"line_id": line_id, "text": ln})
            line_id += 1

    return kept
