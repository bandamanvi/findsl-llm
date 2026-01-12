from llm.ollama_client import ollama_generate

def repair_to_valid_json(bad_text: str, allowed_line_ids: list[int], model: str = "mistral") -> str:
    allowed_str = ", ".join(map(str, allowed_line_ids))

    prompt = f"""
You must output VALID JSON ONLY (no markdown, no extra text).

Fix the output below to match this schema exactly:
{{
  "risk_level": "low|moderate|high|insufficient_context",
  "key_points": [
    {{"claim": "...", "evidence": [1,2]}}
  ],
  "justification": "..."
}}

CRITICAL RULES:
- evidence must be an array of integers and MUST ONLY use these allowed line_ids: [{allowed_str}]
- Do not invent citations.
- If there is insufficient evidence for a claim, remove the claim or set risk_level to "insufficient_context".

TEXT TO FIX:
{bad_text}
""".strip()

    return ollama_generate(prompt, model=model)
