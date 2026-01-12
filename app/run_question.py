import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import json
from datetime import datetime

from app.ask import parse_question
from retriever.loader import load_company_text
from refiner.refine_with_citations import refine_context_with_citations
from llm.prompt_with_citations import build_prompt_with_citations
from llm.ollama_client import ollama_generate
from llm.validate import validate_llm_json
from llm.repair import repair_to_valid_json


def run_from_question(question: str, model: str = "mistral") -> str:
    dsl = parse_question(question)

    ticker = dsl["COMPANY"]["ticker"]
    raw_text = load_company_text(ticker)

    focus = dsl["ANALYSIS"]["focus"]
    context_lines = refine_context_with_citations(raw_text, focus)
    valid_line_ids = {c["line_id"] for c in context_lines}

    prompt = build_prompt_with_citations(dsl, context_lines)

    raw_response = ollama_generate(prompt, model=model)

    try:
        parsed = validate_llm_json(raw_response, valid_line_ids=valid_line_ids)
    except ValueError:
        repaired = repair_to_valid_json(raw_response, allowed_line_ids=sorted(valid_line_ids), model=model)
        parsed = validate_llm_json(repaired, valid_line_ids=valid_line_ids)

    company = ticker.lower()
    analysis_type = dsl["ANALYSIS"]["type"].lower()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = f"output/reports/{company}_{analysis_type}_{ts}.json"

    with open(out_path, "w") as f:
        json.dump(parsed, f, indent=2)

    print(f"✅ Saved report to: {out_path}")
    print(parsed)
    return out_path


if __name__ == "__main__":
    q = input("Ask (include ticker like AAPL/TSLA + focus words like revenue/debt):\n> ")
    run_from_question(q, model="mistral")
