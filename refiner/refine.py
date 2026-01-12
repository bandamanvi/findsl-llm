def refine_context(text: str, focus_areas: list[str]) -> str:
    # Split into non-empty lines
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    # Keep lines that mention any focus keyword
    kept = []
    for ln in lines:
        ln_lower = ln.lower()
        if any(key.lower() in ln_lower for key in focus_areas):
            kept.append(ln)

    return "\n".join(kept)
