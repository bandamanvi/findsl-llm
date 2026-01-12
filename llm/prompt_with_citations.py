import json
from typing import List, Dict

def build_prompt_with_citations(dsl: dict, context_lines: List[Dict]) -> str:
    dsl_json = json.dumps(dsl, indent=2)

    context_block = "\n".join([f"[{c['line_id']}] {c['text']}" for c in context_lines])

    return f"""
You are a careful financial analyst.

RULES:
- Use ONLY the information in CONTEXT_LINES.
- Every key point MUST include evidence as a list of line_ids from CONTEXT_LINES.
- If the context is insufficient, set risk_level to "insufficient_context".
- Output MUST be valid JSON ONLY (no markdown, no extra text).

CONTEXT_LINES:
{context_block}

DSL (task spec):
{dsl_json}

Return JSON with EXACTLY these keys:
- risk_level: one of ["low","moderate","high","insufficient_context"]
- key_points: array of objects, each:
    - claim: short bullet string
    - evidence: array of integers (line_ids), e.g. [1] or [1,2]
- justification: short paragraph grounded in CONTEXT_LINES, and include evidence line_ids in parentheses, e.g. "(see lines 1,2)".
""".strip()
