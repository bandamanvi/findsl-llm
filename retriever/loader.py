def load_company_text(ticker: str) -> str:
    """
    Loads a raw text document for the given company ticker.
    Expected file: data/raw/{ticker_lower}.txt
    """
    path = f"data/raw/{ticker.lower()}.txt"
    with open(path, "r") as f:
        return f.read()
