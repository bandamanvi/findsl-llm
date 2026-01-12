import json

def build_prompt(dsl: dict, refined_context: str) -> str:
    dsl_json = json.dumps(dsl, indent=2)

    return f"""
You are a careful financial analyst.

RULES:
- Use ONLY the information in CONTEXT.
- If the CONTEXT does not contain enough information, say "insufficient_context".
- Do NOT add facts that are not explicitly present in CONTEXT.
- Output MUST be valid JSON.

CONTEXT:
{refined_context}

DSL (task spec):
{dsl_json}

Return JSON with exactly these keys:
- risk_level: one of ["low","moderate","high","insufficient_context"]
- key_points: array of short bullet strings
- justification: short paragraph grounded in CONTEXT
""".strip()
