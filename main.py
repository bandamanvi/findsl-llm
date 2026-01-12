import argparse
import json
from datetime import datetime

from dsl.parser import load_dsl
from refiner.refine_with_citations import refine_context_with_citations
from llm.prompt_with_citations import build_prompt_with_citations

from llm.ollama_client import ollama_generate
from llm.validate import validate_llm_json
from llm.repair import repair_to_valid_json
from retriever.loader import load_company_text



def run(dsl_path: str, model: str = "mistral") -> str:
    dsl = load_dsl(dsl_path)

    ticker = dsl["COMPANY"]["ticker"]
    raw_text = load_company_text(ticker)


    focus = dsl["ANALYSIS"]["focus"]
    context_lines = refine_context_with_citations(raw_text, focus)
    valid_line_ids = {c["line_id"] for c in context_lines}

    prompt = build_prompt_with_citations(dsl, context_lines)





    raw_response = ollama_generate(prompt, model=model)

    try:
        #parsed = validate_llm_json(raw_response)
        parsed = validate_llm_json(raw_response, valid_line_ids=valid_line_ids)

    except ValueError:
        repaired = repair_to_valid_json(raw_response, allowed_line_ids=sorted(valid_line_ids), model=model)

        #repaired = repair_to_valid_json(raw_response, model=model)
        #parsed = validate_llm_json(repaired)
        parsed = validate_llm_json(repaired, valid_line_ids=valid_line_ids)


    company = dsl["COMPANY"]["ticker"].lower()
    analysis_type = dsl["ANALYSIS"]["type"].lower()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = f"output/reports/{company}_{analysis_type}_{ts}.json"

    with open(out_path, "w") as f:
        json.dump(parsed, f, indent=2)

    print(f"✅ Saved report to: {out_path}")
    print(parsed)
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dsl", default="dsl/examples/apple.yaml", help="Path to a DSL YAML file")
    parser.add_argument("--model", default="mistral", help="Ollama model name (e.g., mistral)")
    args = parser.parse_args()

    run(args.dsl, args.model)
