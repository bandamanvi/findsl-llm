# FinDSL-LLM: DSL-Guided Financial Risk Analysis using LLMs

## Overview

FinDSL-LLM is a domain-specific Large Language Model (LLM) system that performs financial risk analysis using a custom Domain-Specific Language (DSL). Instead of functioning as a general chatbot, the system interprets structured financial analysis requests, retrieves relevant company information, refines the context, and generates grounded, structured risk assessments.

The project focuses on improving the reliability of LLM outputs through context filtering, citation validation, structured prompting, and automatic output repair.

---

## Features

- Domain-Specific Language (DSL) for defining financial analysis tasks
- Context refinement based on analysis focus (Revenue, Debt, etc.)
- Local LLM inference using Ollama
- Structured JSON output generation
- Automatic JSON validation and repair
- Line-level evidence citations for explainability
- Natural language query support
- Evaluation pipeline for testing multiple analysis cases

---

## Project Structure

```
findsl-llm/
│
├── app/
│   ├── ask.py
│   └── run_question.py
│
├── data/
│   └── raw/
│
├── dsl/
│   ├── parser.py
│   └── examples/
│
├── llm/
│   ├── ollama_client.py
│   ├── prompt.py
│   ├── prompt_with_citations.py
│   ├── repair.py
│   └── validate.py
│
├── refiner/
│   ├── refine.py
│   └── refine_with_citations.py
│
├── retriever/
│
├── output/
│
├── eval/
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Workflow

The system follows the pipeline below:

```
User Question / DSL
        │
        ▼
 Parse DSL Request
        │
        ▼
Retrieve Company Document
        │
        ▼
Refine Context
        │
        ▼
Generate Prompt
        │
        ▼
Ollama LLM
        │
        ▼
Validate JSON Output
        │
   Invalid?
    /      \
  Yes       No
  │          │
Repair      Save Report
  │
Validate Again
```

---

## Example DSL

```yaml
COMPANY:
  name: Apple
  ticker: AAPL
  period: 2023_Q3

ANALYSIS:
  type: risk_assessment
  focus:
    - revenue
    - debt
```

---

## Example Question

```
Assess AAPL risk focusing on revenue and debt
```

---

## Running the Project

### Run using a DSL file

```bash
python main.py --dsl dsl/examples/apple.yaml
```

### Run using Natural Language

```bash
python app/run_question.py
```

### Run Evaluation

```bash
python eval/run_eval.py
```

---

## Sample Output

```json
{
  "risk_level": "moderate",
  "key_points": [
    {
      "claim": "Revenue growth was modest.",
      "evidence": [1]
    },
    {
      "claim": "Long-term debt may reduce financial flexibility.",
      "evidence": [2]
    }
  ],
  "justification": "The assessment is based only on the retrieved financial context."
}
```

---

## Technologies Used

- Python
- Ollama
- Mistral LLM
- YAML
- JSON
- Prompt Engineering
- NLP
- Context Refinement
- DSL (Domain-Specific Language)

---

## Future Improvements

- Retrieval-Augmented Generation (RAG) with vector databases
- Support for multiple financial reports
- Comparative company analysis
- Healthcare DSL extension
- Web interface using Streamlit or React
- Benchmarking across multiple LLMs

---

## Key Learning Outcomes

Through this project I learned:

- Building domain-specific LLM applications
- Designing DSLs for structured AI workflows
- Prompt engineering for reliable outputs
- Context refinement to reduce hallucinations
- JSON schema validation and automatic repair
- Explainable AI through citation-based responses
- End-to-end LLM system design

---

## Author

**Manvi Banda**

Master's in Data Science  
University of Maryland, College Park