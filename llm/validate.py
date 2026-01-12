import json

REQUIRED_KEYS = {"risk_level", "key_points", "justification"}
ALLOWED_RISK = {"low", "moderate", "high", "insufficient_context"}

def validate_llm_json(text: str, valid_line_ids=None) -> dict:
    """
    valid_line_ids: optional set of allowed citation line_ids.
    If provided, evidence entries must be a subset of this set.
    """
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e

    if not isinstance(data, dict):
        raise ValueError("JSON must be an object (dictionary).")

    missing = REQUIRED_KEYS - set(data.keys())
    if missing:
        raise ValueError(f"Missing required keys: {sorted(missing)}")

    if data["risk_level"] not in ALLOWED_RISK:
        raise ValueError(f"risk_level must be one of {sorted(ALLOWED_RISK)}")

    kp = data["key_points"]
    if not isinstance(kp, list):
        raise ValueError("key_points must be an array.")

    for i, item in enumerate(kp):
        if not isinstance(item, dict):
            raise ValueError(f"key_points[{i}] must be an object.")
        if "claim" not in item or "evidence" not in item:
            raise ValueError(f"key_points[{i}] must contain 'claim' and 'evidence'.")
        if not isinstance(item["claim"], str):
            raise ValueError(f"key_points[{i}].claim must be a string.")
        ev = item["evidence"]
        if not isinstance(ev, list) or not all(isinstance(x, int) for x in ev):
            raise ValueError(f"key_points[{i}].evidence must be an array of integers.")

        if valid_line_ids is not None:
            bad = [x for x in ev if x not in valid_line_ids]
            if bad:
                raise ValueError(
                    f"key_points[{i}].evidence has invalid line_ids {bad}. "
                    f"Allowed: {sorted(valid_line_ids)}"
                )

    if not isinstance(data["justification"], str):
        raise ValueError("justification must be a string.")

    return data
