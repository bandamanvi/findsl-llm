import sys
from pathlib import Path

# -------------------------------------------------------------------
# Make project root importable
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import json
from datetime import datetime

from dsl.parser import load_dsl
from retriever.loader import load_company_text
from refiner.refine_with_citations import refine_context_with_citations
from llm.prompt_with_citations import build_prompt_with_citations
from llm.ollama_client import ollama_generate
from llm.validate import validate_llm_json
from llm.repair import repair_to_valid_json


def run_one(dsl_path: str, model: str = "mistral") -> dict:
    """
    Run one DSL through the full pipeline and return evaluation stats.
    """
    dsl = load_dsl(dsl_path)

    ticker = dsl["COMPANY"]["ticker"]
    raw_text = load_company_text(ticker)

    focus = dsl["ANALYSIS"]["focus"]
    context_lines = refine_context_with_citations(raw_text, focus)
    valid_line_ids = {c["line_id"] for c in context_lines}

    prompt = build_prompt_with_citations(dsl, context_lines)
    raw_response = ollama_generate(prompt, model=model)

    repaired = False
    try:
        parsed = validate_llm_json(raw_response, valid_line_ids=valid_line_ids)
    except Exception:
        repaired = True
        fixed = repair_to_valid_json(
            raw_response,
            allowed_line_ids=sorted(valid_line_ids),
            model=model,
        )
        parsed = validate_llm_json(fixed, valid_line_ids=valid_line_ids)

    return {
        "dsl_path": dsl_path,
        "ticker": ticker,
        "focus": focus,
        "repaired": repaired,
        "risk_level": parsed.get("risk_level"),
        "key_points_count": len(parsed.get("key_points", [])),
        "output": parsed,
    }


if __name__ == "__main__":
    dsl_paths = [
        "dsl/examples/apple.yaml",
        "dsl/examples/tsla.yaml",
    ]

    results = []
    for p in dsl_paths:
        r = run_one(p, model="mistral")
        results.append(r)
        print(
            f"✅ {p} -> risk_level={r['risk_level']} repaired={r['repaired']}"
        )

    summary = {
        "total": len(results),
        "repaired_count": sum(1 for r in results if r["repaired"]),
        "risk_levels": {
            lvl: sum(1 for r in results if r["risk_level"] == lvl)
            for lvl in ["low", "moderate", "high", "insufficient_context"]
        },
        "results": results,
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = f"eval/results_{ts}.json"

    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n📄 Saved eval results to: {out_path}")
