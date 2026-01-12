import re

SUPPORTED_TICKERS = {"AAPL", "TSLA"}
SUPPORTED_FOCUS = {"revenue", "debt", "supply", "margin"}

def parse_question(q: str) -> dict:
    q_upper = q.upper()

    # ticker detection (simple and safe)
    ticker = None
    for t in SUPPORTED_TICKERS:
        if t in q_upper:
            ticker = t
            break

    # focus detection (simple keyword match)
    focus = []
    q_lower = q.lower()
    for f in SUPPORTED_FOCUS:
        if re.search(rf"\b{re.escape(f)}\b", q_lower):
            focus.append(f)

    if ticker is None:
        raise ValueError(f"Ticker not found. Supported tickers: {sorted(SUPPORTED_TICKERS)}")
    if not focus:
        raise ValueError(f"No focus keywords found. Supported focus: {sorted(SUPPORTED_FOCUS)}")

    # Build a DSL-like dict (same shape as YAML)
    return {
        "COMPANY": {"name": ticker, "ticker": ticker, "period": "unknown"},
        "ANALYSIS": {"type": "risk_assessment", "focus": focus},
    }

if __name__ == "__main__":
    q = input("Ask a question (include ticker like AAPL/TSLA and focus words like revenue, debt):\n> ")
    dsl = parse_question(q)
    print("\nParsed DSL-like request:\n", dsl)
